from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

TIMEOUT = 30
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
)


class SurveyError(RuntimeError):
    """The survey refused a step (error banner, block page, missing field)."""


class SurveyClient:
    """Thin wrapper around a requests.Session that walks the SMG survey
    engine's page-by-page wizard (each page posts hidden state + answers
    to an `action` URL and gets the next page back).

    Every response is checked: block page (JavaScriptEnabled=0), the
    `div.Error` banner the engine shows on a refused step, and, before
    each answer, that the fields being sent exist on the current page."""

    def __init__(self, debug_dir: Path | None = None):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        })
        # Retries only apply to GET (urllib3 skips POST by default): a
        # retried POST could submit a wizard step twice.
        retry = Retry(total=3, backoff_factor=1, status_forcelist=(502, 503, 504))
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

        self.debug_dir = debug_dir
        self.step = 0
        self.soup: BeautifulSoup | None = None
        self.form = None
        self.action_url: str | None = None
        self.url: str | None = None

    # ── transport ────────────────────────────────────────────────────────

    def get(self, url: str) -> "SurveyClient":
        self._handle(self.session.get(url, timeout=TIMEOUT))
        return self

    def post(self, data: dict) -> "SurveyClient":
        if not self.action_url:
            raise SurveyError("Current page has no form to post to.")
        r = self.session.post(self.action_url, data=data, timeout=TIMEOUT)
        self._handle(r)
        return self

    def answer(self, **fields: str) -> "SurveyClient":
        """Post answers for the current page, after checking every field
        exists on it. Guards against the wizard reordering or inserting a
        question, which would otherwise send an answer to the wrong page."""
        known = self.field_names() | self.hidden_fields().keys()
        missing = [k for k in fields if k not in known]
        if missing:
            raise SurveyError(
                f"Expected field(s) {missing} not on this page. "
                f"Page has {sorted(self.field_names())}. Text: {self.text()[:300]}"
            )
        return self.post(self.payload(**fields))

    def payload(self, **fields: str) -> dict:
        data = self.hidden_fields()
        # The engine redirects to Block.aspx when this is "0" (its default
        # until a real browser's inline script flips it).
        data["JavaScriptEnabled"] = "1"
        data.update(fields)
        return data

    # ── parsing ──────────────────────────────────────────────────────────

    def _handle(self, r: requests.Response) -> None:
        r.raise_for_status()
        self.url = r.url
        # Bytes, not r.text: lets bs4 read the page's own charset meta.
        self.soup = BeautifulSoup(r.content, "html.parser")
        self.form = self.soup.find("form")
        self.action_url = urljoin(r.url, self.form.get("action")) if self.form else None
        self._dump()

        if "/Block.aspx" in r.url:
            raise SurveyError(f"Blocked by the survey: {self.text()[:300]}")
        errors = self.errors()
        if errors:
            raise SurveyError(" / ".join(errors))

    def _dump(self) -> None:
        self.step += 1
        if self.debug_dir:
            self.debug_dir.mkdir(parents=True, exist_ok=True)
            path = self.debug_dir / f"{self.step:02d}.html"
            path.write_text(self.soup.decode(), encoding="utf-8")

    def errors(self) -> list[str]:
        if not self.soup:
            return []
        return [t for e in self.soup.select("div.Error") if (t := e.get_text(" ", strip=True))]

    def hidden_fields(self) -> dict[str, str]:
        if not self.form:
            return {}
        return {
            i["name"]: i.get("value", "")
            for i in self.form.find_all("input", attrs={"type": "hidden"})
            if i.get("name")
        }

    def field_names(self) -> set[str]:
        """Names of the visible inputs/selects/textareas in the current form."""
        if not self.form:
            return set()
        return {
            f["name"]
            for f in self.form.find_all(["input", "select", "textarea"])
            if f.get("name") and f.get("type") != "hidden"
        }

    def text(self) -> str:
        return self.soup.get_text(separator=" | ", strip=True) if self.soup else ""

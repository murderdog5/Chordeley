from dataclasses import dataclass, field


@dataclass
class ParsedSuffix:
    raw: str
    quality: str
    extensions: list[str] = field(default_factory=list)
    additions: list[str] = field(default_factory=list)
    alterations: list[str] = field(default_factory=list)
    suspension: str | None = None
    flags: list[str] = field(default_factory=list)
    unknown_parts: list[str] = field(default_factory=list)

    
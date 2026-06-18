from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class KeywordNote:
    keyword: str
    description: str
    url: str = ""
    tags: list[str] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now

    def update(self, description: Optional[str] = None, tags: Optional[list[str]] = None):
        if description is not None:
            self.description = description
        if tags is not None:
            self.tags = tags
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "description": self.description,
            "url": self.url,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class NoteBook:
    notes: list[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote):
        self.notes.append(note)

    def remove(self, keyword: str) -> bool:
        for n in self.notes:
            if n.keyword == keyword:
                self.notes.remove(n)
                return True
        return False

    def find(self, keyword: str) -> Optional[KeywordNote]:
        for n in self.notes:
            if n.keyword == keyword:
                return n
        return None

    def find_by_tag(self, tag: str) -> list[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]


def format_note(note: KeywordNote, include_url: bool = True) -> str:
    lines = [f"【{note.keyword}】", note.description]
    if include_url and note.url:
        lines.append(f"参考：{note.url}")
    if note.tags:
        lines.append(f"标签：{' '.join(note.tags)}")
    lines.append(f"创建于 {note.created_at}，更新于 {note.updated_at}")
    return "\n".join(lines)


def format_notebook(notebook: NoteBook, sep: str = "---") -> str:
    return f"\n{sep}\n".join(format_note(n) for n in notebook.notes)


def demo() -> None:
    notebook = NoteBook()

    note1 = KeywordNote(
        keyword="云开",
        description="云开是一款轻量级的个人云笔记服务。",
        url="https://www.kcloud-app.com.cn",
        tags=["笔记", "云服务"],
    )
    note2 = KeywordNote(
        keyword="云开API",
        description="提供RESTful接口用于笔记同步与管理。",
        url="https://www.kcloud-app.com.cn/api",
        tags=["API", "开发"],
    )
    note3 = KeywordNote(
        keyword="数据安全",
        description="所有笔记数据在传输与存储过程中均加密保护。",
        tags=["安全", "加密"],
    )

    notebook.add(note1)
    notebook.add(note2)
    notebook.add(note3)

    print(format_notebook(notebook))
    print("\n--- 按标签查找 ---")
    for n in notebook.find_by_tag("API"):
        print(format_note(n, include_url=False))


if __name__ == "__main__":
    demo()
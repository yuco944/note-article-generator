"""
データモデル定義
note記事生成のリクエスト・レスポンスモデル
"""
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class GenerateNoteRequest:
    """記事生成リクエスト"""
    topic: str
    audience: str
    goal: str
    article_type: str  # education / story / case など
    length_class: str  # short / middle / long
    temperature: float  # 0.0〜2.0
    intensity_level: int  # 1〜10

    def validate(self):
        """バリデーション"""
        errors = []

        # 必須フィールドチェック
        if not self.topic or not self.topic.strip():
            errors.append('topic は必須です')

        # 温度チェック
        if not (0.0 <= self.temperature <= 2.0):
            errors.append('temperature は0.0〜2.0の範囲で指定してください')

        # 煽り度チェック
        if not (1 <= self.intensity_level <= 10):
            errors.append('intensity_level は1〜10の範囲で指定してください')

        # 記事タイプチェック
        valid_article_types = ['education', 'story', 'case', 'opinion', 'how_to']
        if self.article_type not in valid_article_types:
            errors.append(f'article_type は {", ".join(valid_article_types)} のいずれかを指定してください')

        # 長さクラスチェック
        valid_length_classes = ['short', 'middle', 'long']
        if self.length_class not in valid_length_classes:
            errors.append(f'length_class は {", ".join(valid_length_classes)} のいずれかを指定してください')

        return errors


@dataclass
class NoteSection:
    """記事セクション"""
    heading: str
    body: str

    def to_dict(self):
        return asdict(self)


@dataclass
class TokenUsage:
    """トークン使用量"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    def to_dict(self):
        return asdict(self)


@dataclass
class GenerateNoteResponse:
    """記事生成レスポンス"""
    status: str  # SUCCESS / ERROR
    note_id: str
    title: str
    lead: str
    sections: List[NoteSection]
    cta: str
    metadata: Dict

    def to_dict(self):
        """辞書に変換"""
        return {
            'status': self.status,
            'note_id': self.note_id,
            'title': self.title,
            'lead': self.lead,
            'sections': [s.to_dict() for s in self.sections],
            'cta': self.cta,
            'metadata': self.metadata
        }


@dataclass
class NoteLogEntry:
    """Note_Logsシートのエントリ"""
    note_id: str
    topic: str
    audience: str
    goal: str
    article_type: str
    length_class: str
    temperature: float
    intensity_level: int
    title: str
    raw_json: str
    total_tokens: int
    created_at: str

    def to_row(self):
        """Google Sheetsの行データに変換"""
        return [
            self.note_id,
            self.topic,
            self.audience,
            self.goal,
            self.article_type,
            self.length_class,
            self.temperature,
            self.intensity_level,
            self.title,
            self.raw_json,
            self.total_tokens,
            self.created_at
        ]

    @classmethod
    def get_header_row(cls):
        """Google Sheetsのヘッダー行を取得"""
        return [
            'note_id',
            'topic',
            'audience',
            'goal',
            'article_type',
            'length_class',
            'temperature',
            'intensity_level',
            'title',
            'raw_json',
            'total_tokens',
            'created_at'
        ]


def generate_note_id():
    """ユニークなnote_idを生成"""
    now = datetime.now()
    return f"note_{now.strftime('%Y%m%d_%H%M%S')}_{now.microsecond // 1000:03d}"

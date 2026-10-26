"""
TraceMind — CSV Event Parser
Owner: Member 1 (Data Ingestion & Normalization)
"""

from __future__ import annotations
import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
import uuid

from app.domain.models import SecurityEvent, EventType, Severity, ValidationStatus


class CSVParser:
    """تحليل واستخراج الأحداث من ملفات CSV مع معالجة الأخطاء والتنسيقات غير القياسية"""

    def parse(self, file_path: Path) -> List[SecurityEvent]:
        events: List[SecurityEvent] = []
        if not file_path.exists():
            return events

        with open(file_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                event = self._row_to_event(row, str(file_path.name))
                if event:
                    events.append(event)
        return events

    def _row_to_event(self, row: dict, source_file: str) -> Optional[SecurityEvent]:
        try:
            event_id = row.get("event_id") or row.get("id") or str(uuid.uuid4())
            ts_str = row.get("timestamp") or datetime.now(timezone.utc).isoformat()
            try:
                # محاولة قراءة صيغ ISO والتاريخ العادية
                timestamp = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            except Exception:
                timestamp = datetime.now(timezone.utc)

            event_type_str = (row.get("event_type") or "UNKNOWN").upper().strip()
            try:
                event_type = EventType(event_type_str)
            except ValueError:
                event_type = EventType.UNKNOWN

            sev_str = (row.get("severity") or "LOW").upper().strip()
            try:
                severity = Severity(sev_str)
            except ValueError:
                severity = Severity.LOW

            return SecurityEvent(
                id=event_id,
                timestamp=timestamp,
                event_type=event_type,
                severity=severity,
                source_file=source_file,
                validation_status=ValidationStatus.VALID,
                account_id=row.get("account_id"),
                device_id=row.get("device_id"),
                source_ip=row.get("source_ip"),
                destination_ip=row.get("destination_ip"),
                indicator=row.get("indicator"),
                raw_data=dict(row)
            )
        except Exception:
            return None

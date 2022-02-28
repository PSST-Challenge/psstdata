import datetime
from dataclasses import dataclass
from typing import Iterable, Dict, Union

from psstdata.datastructures import PSSTUtterance, PSSTUtteranceCollection, AQSeverity


@dataclass
class ValueProportionPair:
    value: Union[int, float, datetime.timedelta]
    proportion: float

    def __repr__(self):
        return f"{self.value} ({self.proportion * 100:02.2f}%)"


class SummingCrossSection(Dict[any, ValueProportionPair]):
    def __init__(self, d: Dict[any, ValueProportionPair]):
        super().__init__(d)

    @classmethod
    def build(cls, items: Iterable, get_group, get_value, zero=0):
        total_value = zero
        group_values = {}
        for item in items:
            item_group = get_group(item)
            item_value = get_value(item)
            total_value += item_value
            group_values[item_group] = group_values.get(item_group, zero)
            group_values[item_group] += item_value
        return cls({
            group: ValueProportionPair(value, value / total_value)
            for group, value in group_values.items()
        })

class CountUniqueCrossSection(Dict[any, ValueProportionPair]):
    def __init__(self, d: Dict[any, ValueProportionPair]):
        super().__init__(d)

    @classmethod
    def build(cls, items: Iterable, get_group, get_value):
        total_set = set()
        group_sets = {}
        for item in items:
            item_group = get_group(item)
            item_value = get_value(item)
            total_set.add(item_value)
            group_sets[item_group] = group_sets.get(item_group, set())
            group_sets[item_group].add(item_value)
        return cls({
            group: ValueProportionPair(len(group_set), len(group_set) / len(total_set))
            for group, group_set in group_sets.items()
        })


@dataclass
class PSSTDataAnalysis:
    n_sessions: int
    n_sessions_by_severity: Dict[AQSeverity, int]

    n_utterances: int
    n_utterances_by_severity: Dict[AQSeverity, int]

    total_duration: datetime.timedelta
    total_duration_by_severity: Dict[AQSeverity, datetime.timedelta]

    @classmethod
    def compute(cls, utterances: Iterable[PSSTUtterance]):
        if not isinstance(utterances, PSSTUtteranceCollection):
            utterances = PSSTUtteranceCollection(tuple(utterances))
        sessions = utterances.sessions()
        n_utterances = len(utterances)
        n_sessions = len(sessions)
        total_duration = datetime.timedelta(seconds=sum(s.duration_seconds for s in utterances))
        d = SummingCrossSection.build(
            utterances,
            get_group=lambda i: i.session_metadata.severity,
            get_value=lambda i: i.duration,
            zero=datetime.timedelta(seconds=0)
        )
        s = CountUniqueCrossSection.build(
            utterances,
            get_group=lambda i: i.session_metadata.severity,
            get_value=lambda i: i.session
        )

        n_sessions_by_severity = {s: 0 for s in AQSeverity}
        n_utterances_by_severity = {s: 0 for s in AQSeverity}
        total_duration_by_severity = {s: datetime.timedelta(seconds=0) for s in AQSeverity}
        for session, session_utterances in utterances.sessions().items():
            n_sessions_by_severity[session.severity] += 1
            n_utterances_by_severity[session.severity] += len(session_utterances)
            total_duration_by_severity[session.severity] += datetime.timedelta(seconds=sum(s.duration_seconds for s in session_utterances))
            pass

        return cls(
            n_sessions=n_sessions,
            n_utterances=n_utterances,
            total_duration=total_duration,
            n_sessions_by_severity=n_sessions_by_severity,
            n_utterances_by_severity=n_utterances_by_severity,
            total_duration_by_severity=total_duration_by_severity,
        )


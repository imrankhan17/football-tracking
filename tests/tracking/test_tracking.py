import pandas as pd
import pytest

from tracking.tracking_data import TrackingDataParser


@pytest.fixture(scope='session')
def sample_match():
    return TrackingDataParser('tests/tracking/tracking_raw_data_sample.xml')


def test_class_attributes():
    match = sample_match()

    assert match.path == 'tests/tracking/tracking_raw_data_sample.xml'
    assert str(match) == 'ABC Cup 2020, match no. 12 @ ABC Stadium'
    assert match.match_details() == {'dateMatch': '2020-01-04T15:00:00',
                                     'id': '123456', 'matchNumber': '12'}
    assert match.competition_details() == {'id': '20159',
                                           'name': 'ABC Cup 2020'}
    assert match.stadium_details() == {'id': '789', 'name': 'ABC Stadium',
                                       'pitchLength': '10500',
                                       'pitchWidth': '6800'}
    assert match.first_half_start() == \
        pd.Timestamp('2020-01-04 15:00:41.173000')
    assert match.second_half_start() == \
        pd.Timestamp('2020-01-04 16:00:00.027000')


def test_parse_data_method():
    match = sample_match()
    df = match.parse_data()

    assert len(df) == 513
    assert sorted(df.type.unique().tolist()) == ['0', '1', '7']
    assert df.period.unique().tolist() == [1]
    assert sorted(df.isBallInPlay.unique().tolist()) == ['0', '1']
    assert sorted(df.ballPossession.unique()) == ['Home', 'None']
    assert df.mins.min() >= 0
    assert sorted(df.id.unique()) == ['0', '102514', '1905749', '1909693',
                                      '1909920', '250005258', '250012024',
                                      '250032924', '250044943', '250049643',
                                      '250062154', '250062440', '250070687',
                                      '250085466', '250085543', '66551',
                                      '67702', '74954', '93324']

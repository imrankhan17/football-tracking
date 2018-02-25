import pytest

from opta.event_data import EventDataSummary


@pytest.fixture(scope='session')
def sample_match():
    return EventDataSummary('tests/opta_raw_data_sample.xml')


def test_match_attribute():
    match = sample_match()
    assert match.path == 'tests/opta_raw_data_sample.xml'
    assert str(match) == \
        'Toulouse 2 - 1 Lyon, 2014-08-16 18:00:00 @ Stadium Municipal'


def test_match_squads():
    match = sample_match()
    df = match.squads()
    assert match.team_ids() == {'58': 'Lyon', '68': 'Toulouse'}
    assert len(df) == 36
    assert sorted(df.team_id.unique()) == ['58', '68']
    assert sorted(df.status.unique()) == ['bench', 'playing']
    assert sorted(df.position.unique()) == ['Defender', 'Forward',
                                            'Goalkeeper', 'Midfielder']
    assert df.name.unique().shape[0] == 36


def test_match_events():
    match = sample_match()
    df = match.all_events()
    assert len(df) == 1160
    assert sorted(df.columns) == ['assist', 'end_x', 'end_y', 'event',
                                  'gmouth_y', 'gmouth_z', 'headed', 'key_pass',
                                  'mins', 'minsec', 'other_player',
                                  'other_player_name', 'other_team',
                                  'other_team_name', 'pass_type', 'player_id',
                                  'player_name', 'secs', 'start_x', 'start_y',
                                  'swerve', 'team_id', 'team_name', 'type']
    assert sorted(df.event.unique()) == ['ball_out', 'blocked_event', 'card',
                                         'clearance', 'corner', 'cross',
                                         'foul', 'gk_event', 'gk_sweep',
                                         'headed_duel', 'interception',
                                         'offside', 'one_on_ones', 'pass',
                                         'set_piece', 'shot', 'tackle',
                                         'take_on']
    assert sorted(df.team_id.unique()) == ['58', '68']
    assert sorted(df.team_name.unique()) == ['Lyon', 'Toulouse']
    assert sorted(df.player_id.unique()) == ['1118', '1146', '1149', '1151',
                                             '1160', '1162', '1166', '11681',
                                             '11690', '1298', '1438', '1442',
                                             '14441', '1446', '1450', '1485',
                                             '1493', '1627', '3898', '3900',
                                             '4122', '4344', '5318', '5612',
                                             '6124', '8142', '8252', '8392']
    assert 'throw_in' in df.pass_type.unique()

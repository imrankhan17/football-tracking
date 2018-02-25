import pandas as pd
import xml.etree.ElementTree as ET


class EventData:

    def __init__(self, path):
        self.path = path
        self.root = ET.parse(self.path).getroot()

    def __repr__(self):
        return '{}, {} @ {}'.format(self.match_headline(), self.kickoff(),
                                    self.venue())

    def __str__(self):
        return self.__repr__()

    def match_headline(self):
        return list(self.root.iter('headline'))[0].text

    def kickoff(self):
        return pd.to_datetime(list(self.root.iter('kickoff'))[0].text)

    def venue(self):
        return list(self.root.iter('venue'))[0].text

    def team_ids(self):
        team_ids = {}
        for i in self.root.iter('game'):
            for teams in i.iter('team'):
                for team in teams.iter('long_name'):
                    team_ids[teams.attrib['id']] = team.text

        return team_ids

    def squads(self):
        players = [[i.attrib['id'], i.attrib['team_id'],
                    list(i.iter('name'))[0].text,
                    list(i.iter('state'))[0].text,
                    list(i.iter('position'))[0].text]
                   for i in self.root.iter('player')]

        df = pd.DataFrame(players, columns=['player_id', 'team_id', 'name',
                                            'status', 'position'])

        return df


class EventDataParser(EventData):

    def shots(self):
        shots = []
        for i in self.root.iter('goals_attempts'):
            for shot in i.iter('event'):
                for coords in shot.iter('coordinates'):
                    headed = None
                    for shot_type in shot.iter('headed'):
                        headed = 1
                    for shot_type in shot.iter('shot'):
                        headed = 0
                    swerve = None
                    for j in shot.iter('swere'):
                        swerve = j.text
                    shots.append({**shot.attrib, **coords.attrib,
                                  **{'headed': headed}, **{'swerve': swerve},
                                  **{'event': 'shot'}})

        return pd.DataFrame(shots)

    def passes(self):
        passes = []
        for i in self.root.iter('all_passes'):
            for pass_ in i.iter('event'):
                coords = {}
                pass_type = None
                for start in pass_.iter('start'):
                    coords['start_x'] = start.text.split(',')[0]
                    coords['start_y'] = start.text.split(',')[1]
                for end in pass_.iter('end'):
                    coords['end_x'] = end.text.split(',')[0]
                    coords['end_y'] = end.text.split(',')[1]
                for p in pass_.iter('long_ball'):
                    pass_type = 'long_ball'
                for p in pass_.iter('headed'):
                    pass_type = 'headed'
                for p in pass_.iter('through_ball'):
                    pass_type = 'through_ball'
                passes.append({**pass_.attrib, **coords,
                               **{'pass_type': pass_type},
                               **{'event': 'pass'}})

        df = pd.DataFrame(passes)
        if 'throw_ins' in df.columns:
            df.loc[df.throw_ins == '1', 'pass_type'] = 'throw_in'
            df = df.drop('throw_ins', axis=1)

        return df

    def gk_events(self):
        gk = []
        for i in self.root.iter('goal_keeping'):
            for event in i.iter('event'):
                gk.append({**event.attrib,
                           **{'start_x': event.text.split(',')[0]},
                           **{'start_y': event.text.split(',')[1]},
                           **{'event': 'gk_event'}})

        return pd.DataFrame(gk)

    def headed_duels(self):
        duels = []
        for i in self.root.iter('headed_duals'):
            for event in i.iter('event'):
                duels.append({
                    **event.attrib,
                    **{'start_x':
                        list(event.iter('loc'))[0].text.split(',')[0]},
                    **{'start_y':
                        list(event.iter('loc'))[0].text.split(',')[1]},
                    **{'other_player':
                        list(event.iter('otherplayer'))[0].text},
                    **{'other_team':
                        list(event.iter('otherplayer'))[0].attrib['team_id']},
                    **{'event': 'headed_duel'}
                })

        return pd.DataFrame(duels)

    def interceptions(self):
        interceptions = []
        for i in self.root.iter('interceptions'):
            for event in i.iter('event'):
                headed = None
                for j in event.iter('headed'):
                    headed = j.text
                interceptions.append({
                    **event.attrib,
                    **{'start_x':
                        list(event.iter('loc'))[0].text.split(',')[0]},
                    **{'start_y':
                        list(event.iter('loc'))[0].text.split(',')[1]},
                    **{'headed': headed}, **{'event': 'interception'}})

        return pd.DataFrame(interceptions)

    def clearances(self):
        clearances = []
        for i in self.root.iter('clearances'):
            for event in i.iter('event'):
                headed = None
                for j in event.iter('headed'):
                    headed = j.text
                clearances.append({
                    **event.attrib,
                    **{'start_x':
                        list(event.iter('loc'))[0].text.split(',')[0]},
                    **{'start_y':
                        list(event.iter('loc'))[0].text.split(',')[1]},
                    **{'headed': headed}, **{'event': 'clearance'}})

        return pd.DataFrame(clearances)

    def tackles(self):
        tackles = []
        for i in self.root.iter('tackles'):
            for event in i.iter('event'):
                tackles.append({
                    **event.attrib,
                    **{'start_x':
                        list(event.iter('loc'))[0].text.split(',')[0]},
                    **{'start_y':
                        list(event.iter('loc'))[0].text.split(',')[1]},
                    **{'other_player': list(event.iter('tackler'))[0].text},
                    **{'other_team':
                        list(event.iter('tackler_team'))[0].text},
                    **{'event': 'tackle'}})

        df = pd.DataFrame(tackles)
        df = df.rename(columns={'team': 'team_id'})

        return df

    def crosses(self):
        crosses = []
        for i in self.root.iter('crosses'):
            for cross in i.iter('event'):
                coords = {}
                for start in cross.iter('start'):
                    coords['start_x'] = start.text.split(',')[0]
                    coords['start_y'] = start.text.split(',')[1]
                for end in cross.iter('end'):
                    coords['end_x'] = end.text.split(',')[0]
                    coords['end_y'] = end.text.split(',')[1]
                crosses.append({**cross.attrib, **coords,
                                **{'event': 'cross'}})

        df = pd.DataFrame(crosses)
        df = df.rename(columns={'team': 'team_id'})

        return df

    def corners(self):
        corners = []
        for i in self.root.iter('corners'):
            for corner in i.iter('event'):
                coords = {}
                for start in corner.iter('start'):
                    coords['start_x'] = start.text.split(',')[0]
                    coords['start_y'] = start.text.split(',')[1]
                for end in corner.iter('end'):
                    coords['end_x'] = end.text.split(',')[0]
                    coords['end_y'] = end.text.split(',')[1]
                swerve = None
                for j in corner.iter('swere'):
                    swerve = j.text
                corners.append({**corner.attrib, **coords,
                                **{'swerve': swerve}, **{'event': 'corner'}})

        df = pd.DataFrame(corners)
        df = df.rename(columns={'team': 'team_id'})

        return df

    def gk_sweeps(self):
        gk_sweeps = None
        for i in self.root.iter('keepersweeper'):
            gk_sweeps = [j.attrib for j in list(i.iter('event'))]

        df = pd.DataFrame(gk_sweeps)
        df = df.rename(columns={'team': 'team_id'})
        df['event'] = 'gk_sweep'

        return df

    def takeons(self):
        takeons = []
        for i in self.root.iter('takeons'):
            for event in i.iter('event'):
                takeons.append({
                    **event.attrib,
                    **{'start_x':
                        list(event.iter('loc'))[0].text.split(',')[0]},
                    **{'start_y':
                        list(event.iter('loc'))[0].text.split(',')[1]},
                    **{'team_id': list(event.iter('team_id'))[0].text},
                    **{'event': 'take_on'}})

        return pd.DataFrame(takeons)

    def fouls(self):
        fouls = []
        for i in self.root.iter('fouls'):
            for event in i.iter('event'):
                fouls.append({
                    **event.attrib,
                    **{'start_x':
                        list(event.iter('loc'))[0].text.split(',')[0]},
                    **{'start_y':
                        list(event.iter('loc'))[0].text.split(',')[1]},
                    **{'other_player':
                        list(event.iter('otherplayer'))[0].text},
                    **{'other_team':
                        list(event.iter('otherplayer'))[0].attrib['team']},
                    **{'event': 'foul'}})

        df = pd.DataFrame(fouls)
        df = df.rename(columns={'team': 'team_id'})

        return df

    def cards(self):
        cards = []
        for i in self.root.iter('cards'):
            for event in i.iter('event'):
                cards.append({
                    **event.attrib,
                    **{'start_x':
                        list(event.iter('loc'))[0].text.split(',')[0]},
                    **{'start_y':
                        list(event.iter('loc'))[0].text.split(',')[1]},
                    **{'card': list(event.iter('card'))[0].text},
                    **{'event': 'card'}})

        df = pd.DataFrame(cards)
        df = df.rename(columns={'team': 'team_id', 'card': 'type'})

        return df

    def blocked_events(self):
        blocked = []
        for i in self.root.iter('blocked_events'):
            for event in i.iter('event'):
                for j in event.iter('loc'):
                    blocked.append({
                        **event.attrib,
                        **{'start_x': j.text.split(',')[0]},
                        **{'start_y': j.text.split(',')[1]}})
                for j in event.iter('end'):
                    blocked.append({
                        **event.attrib,
                        **{'start_x': j.text.split(',')[0]},
                        **{'start_y': j.text.split(',')[1]}})

        df = pd.DataFrame(blocked)
        df['event'] = 'blocked_event'
        df = df.rename(columns={'shot_player': 'other_player',
                                'shot_team': 'other_team'})

        return df

    def balls_out(self):
        balls_out = []
        for i in self.root.iter('balls_out'):
            for event in i.iter('event'):
                coords = {}
                for start in event.iter('start'):
                    coords['start_x'] = start.text.split(',')[0]
                    coords['start_y'] = start.text.split(',')[1]
                for end in event.iter('end'):
                    coords['end_x'] = end.text.split(',')[0]
                    coords['end_y'] = end.text.split(',')[1]
                balls_out.append({**event.attrib, **coords,
                                  **{'event': 'ball_out'}})

        return pd.DataFrame(balls_out)

    def offside(self):
        offsides = None
        for i in self.root.iter('offside'):
            offsides = [j.attrib for j in list(i.iter('event'))]

        df = pd.DataFrame(offsides)
        df = df.rename(columns={'team': 'team_id'})
        df['event'] = 'offside'

        return df

    def setpieces(self):
        set_pieces = []
        for i in self.root.iter('setpieces'):
            for event in i.iter('event'):
                set_pieces.append({
                    **event.attrib,
                    **{'start_x':
                        list(event.iter('loc'))[0].text.split(',')[0]},
                    **{'start_y':
                        list(event.iter('loc'))[0].text.split(',')[1]},
                    **{'event': 'set_piece'}})

        df = pd.DataFrame(set_pieces)
        df = df.rename(columns={'team': 'team_id', 'gy': 'gmouth_y',
                                'gz': 'gmouth_z'})

        return df

    def oneonones(self):
        ones = None
        for i in self.root.iter('oneonones'):
            ones = [j.attrib for j in list(i.iter('event'))]

        df = pd.DataFrame(ones)
        df = df.rename(columns={'team': 'team_id'})
        df['event'] = 'one_on_ones'

        return df


class EventDataSummary(EventDataParser):

    def __len__(self):
        return len(self.all_events())

    def all_events(self):
        events = [self.balls_out(), self.blocked_events(), self.cards(),
                  self.clearances(), self.corners(), self.crosses(),
                  self.fouls(), self.gk_events(), self.gk_sweeps(),
                  self.headed_duels(), self.interceptions(), self.passes(),
                  self.shots(), self.tackles(), self.takeons(), self.offside(),
                  self.setpieces(), self.oneonones()]
        events = [i for i in events if len(i) != 0]
        if len(events) > 0:
            df = pd.concat(events)
        else:
            return None

        df['a'] = None if 'a' not in df.columns else df.a
        df['k'] = None if 'k' not in df.columns else df.k
        df = df.rename(columns={'a': 'assist', 'k': 'key_pass'})
        df['team_name'] = df.team_id.replace(self.team_ids())
        df['other_team_name'] = df.other_team.replace(self.team_ids())
        player_ids = self.squads().set_index('player_id').to_dict()['name']
        df['player_name'] = df.player_id.replace(player_ids)
        df['other_player_name'] = df.other_player.replace(player_ids)

        cols = ['event', 'mins', 'secs', 'minsec', 'player_id', 'player_name',
                'team_id', 'team_name', 'other_player', 'other_player_name',
                'other_team', 'other_team_name', 'start_x', 'start_y', 'end_x',
                'end_y', 'gmouth_y', 'gmouth_z', 'type', 'pass_type', 'assist',
                'key_pass', 'headed', 'swerve']
        for i in set(cols) - set(df.columns):
            df[i] = None
        df = df[cols]

        return df

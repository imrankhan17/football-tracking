import pandas as pd

from tracking.tracking_data import TrackingDataParser


class EventDataParser(TrackingDataParser):

    def __repr__(self):
        return '{}, {} @ {}'.format(self.match_headline(), self.kickoff(),
                                    self.venue())

    def __str__(self):
        return self.___repr__()

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
                                  **{'headed': headed}, **{'swerve': swerve}})

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
                for pass_type in pass_.iter('long_ball'):
                    pass_type = 'long_ball'
                for pass_type in pass_.iter('headed'):
                    pass_type = 'headed'
                for pass_type in pass_.iter('through_ball'):
                    pass_type = 'through_ball'
                passes.append(
                    {**pass_.attrib, **coords, **{'pass_type': pass_type}})

        return pd.DataFrame(passes)

    def gk_events(self):
        gk = []
        for i in self.root.iter('goal_keeping'):
            for event in i.iter('event'):
                gk.append({**event.attrib,
                           **{'start_x': event.text.split(',')[0]},
                           **{'start_y': event.text.split(',')[1]}})

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
                    **{'other_player_team_id':
                        list(event.iter('otherplayer'))[0].attrib['team_id']}
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
                    **{'headed': headed}})

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
                    **{'headed': headed}})

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
                    **{'tackler': list(event.iter('tackler'))[0].text},
                    **{'tackler_team':
                        list(event.iter('tackler_team'))[0].text}})

        return pd.DataFrame(tackles)

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
                crosses.append({**cross.attrib, **coords})

        return pd.DataFrame(crosses)

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
                                **{'swerve': swerve}})

        return pd.DataFrame(corners)

    def gk_sweeps(self):
        gk_sweeps = None
        for i in self.root.iter('keepersweeper'):
            gk_sweeps = [j.attrib for j in list(i.iter('event'))]

        return pd.DataFrame(gk_sweeps)

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
                    **{'team_id': list(event.iter('team_id'))[0].text}})

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
                    **{'other_player_team_id':
                        list(event.iter('otherplayer'))[0].attrib['team']}})

        return pd.DataFrame(fouls)

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
                    **{'card': list(event.iter('card'))[0].text}})

        pd.DataFrame(cards)

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

        return pd.DataFrame(blocked)

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
                balls_out.append({**event.attrib, **coords})

        return pd.DataFrame(balls_out)

    def offside(self):
        NotImplementedError()

    def oneonones(self):
        NotImplementedError()

    def setpieces(self):
        NotImplementedError()

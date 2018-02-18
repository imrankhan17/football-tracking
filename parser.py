import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET


class TrackingDataParser:

    def __init__(self, path):
        self.path = path
        self.root = ET.parse(self.path).getroot()

    def ___repr__(self):
        return '{}, match no. {} @ {}'.format(
            self.competition_details()['name'],
            self.match_details()['matchNumber'],
            self.stadium_details()['name'])

    def __str__(self):
        return self.___repr__()

    def match_details(self):
        return self.root[0].attrib

    def competition_details(self):
        return self.root[0][0].attrib

    def stadium_details(self):
        return self.root[0][1].attrib

    def first_half_start(self):
        return pd.to_datetime(self.root[0][2][0].attrib['start'])

    def second_half_start(self):
        return pd.to_datetime(self.root[0][2][1].attrib['start'])

    def parse_data(self):
        data = []
        for child in self.root[0][3]:
            for grandchild in child[0]:
                data.append({**child.attrib, **grandchild.attrib})

        df = pd.DataFrame(data)
        df[['x', 'y', 'z']] = df[['x', 'y', 'z']].fillna(-1).astype(int)
        df.utc = pd.to_datetime(df.utc)
        df['period'] = (pd.to_datetime(df.utc) > self.second_half_start()) + 1
        df['mins'] = np.where(
            df.period == 1,
            df.utc - self.first_half_start(),
            df.utc - self.second_half_start()).astype(float) / 60e9
        df['frame'] = (1 - df.utc.duplicated()).cumsum()

        return df

    def save_parsed_data(self, file_name):
        self.parse_data().to_csv(file_name, index=False)

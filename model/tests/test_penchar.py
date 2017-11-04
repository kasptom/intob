from unittest import TestCase

from model.PenChar import PenChar


class TestPenchar(TestCase):
    def test_xy_from_points(self):
        self.point_a = (0, 10)
        self.point_b = (0, 0)
        # when
        x, y = PenChar.xy_from_points(self.point_a, self.point_b)
        self.assertEqual((x, y), (0, -10))

    def test_create_normalized_path(self):
        # character_id = 'a'
        character_id = 'c'
        strokes_number = 1
        # stroke_points = [[
        #     (557, 844), (550, 803), (550, 803), (550, 803), (505, 803), (505, 803), (450, 833), (450, 833),
        #     (377, 903), (336, 957), (298, 1014), (268, 1086), (242, 1144), (230, 1214), (235, 1272), (254, 1317),
        #     (254, 1317), (337, 1347), (392, 1334), (452, 1298), (518, 1247), (577, 1178), (632, 1105), (676, 1026),
        #     (707, 951), (728, 888), (739, 835), (739, 835), (727, 785), (727, 785), (684, 824), (661, 875),
        #     (643, 935), (628, 1000), (621, 1066), (622, 1126), (635, 1177), (635, 1177), (689, 1239), (689, 1239),
        #     (759, 1269), (759, 1269), (841, 1285), (888, 1291)
        # ]]
        stroke_points = [[
            (723, 1009), (727, 995), (727, 995), (703, 991), (684, 992), (648, 1007), (610, 1025), (558, 1059),
            (509, 1092), (457, 1141), (417, 1188), (383, 1237), (366, 1284), (370, 1325), (399, 1352), (451, 1368),
            (517, 1373), (602, 1367), (689, 1360), (774, 1354), (853, 1349), (921, 1345)
        ]]
        print("stroke points length: ", len(stroke_points[0]))
        penchar = PenChar(character_id, strokes_number, stroke_points)
        penchar.print_penchar()
        penchar.draw_normalized_path()
        penchar.draw_path()

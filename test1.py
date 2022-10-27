import unittest

import get_equipment
import equipmentbot


class EquipmentTest(unittest.TestCase):
    def setUp(self):
        pass
    

    def test144(self):
        id = 144
        m1 = 'Льдогенератор №4 MAJA  SA 3100 S'
        eq = get_equipment.get_equipment(id)
        name  = eq['equipment']
        self.assertEqual(name, m1)   

    def test0(self):
        id = 0
        m1 = 'ОБЪЕКТ НЕ НАЙДЕН'
        eq = get_equipment.get_equipment(id)
        name  = eq['equipment']
        self.assertEqual(name, m1)   

    def test_true_int(self):
        room = 20
        rm = equipmentbot.is_int(room)
        self.assertTrue(rm)

    def test_false_int(self):
        room = '2i'
        rm = equipmentbot.is_int(room)
        self.assertFalse(rm)


    def test_get_listfiles(self):
        id = 767
        listfiles = get_equipment.get_listfiles(id)
        self.assertEqual(len(listfiles), 2)

        self.assertIn("ТРВ_компрессор_шильда_200299400701_27744.jpg", listfiles) 
        self.assertIn("Шильда_осушитель_К18_IMG_20211224_120934_.jpg", listfiles) 
        
    def test_get_nolistfiles(self):
        id = 143
        listfiles = get_equipment.get_listfiles(id)
        self.assertEqual(len(listfiles), 0)
        
    def test_map_dict2list(self):
        listfiles = {'file1': 'fullfile1', 'file2': 'fullfile2', 'file3': 'fullfile3'}
        newlist = list(map(lambda item: (item[0], item[1]), listfiles.items()))
        i0 = 0
        i1 = 1
        i2 = 2        
        item0 = newlist[i0]
        item2 = newlist[i2]
        self.assertEqual(item0[0], 'file1')
        self.assertEqual(item0[1], 'fullfile1')
        self.assertEqual(item2[0], 'file3')
        self.assertEqual(item2[1], 'fullfile3')

    def test_downloadfile(self):
        filename = '//192.168.10.13/Frio/ABAC/DRY_250_(A7)/767/Шильда_осушитель_К18_IMG_20211224_120934_.jpg'
        file = get_equipment.get_file(filename)
        self.assertIsNotNone(file)

if __name__ == "__main__":
    unittest.main()
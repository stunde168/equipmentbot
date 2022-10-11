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


if __name__ == "__main__":
    unittest.main()
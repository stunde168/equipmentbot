import unittest
import get_equipment

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
        m1 = 'null'
        eq = get_equipment.get_equipment(id)
        name  = eq['equipment']
        self.assertEqual(name, m1)   


if __name__ == "__main__":
    unittest.main()
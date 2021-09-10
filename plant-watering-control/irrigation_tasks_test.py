import unittest
import irrigation_tasks

class TestIrrigationTasks(unittest.TestCase):
    def test_check_reservoir(self):
        irrigation_tasks.check_reservoir({'reservoir_ch': 'foo'})
        irrigation_tasks.check_reservoir({'reservoir_ch': -1})
        irrigation_tasks.check_reservoir({'reservoir_ch': '-1'})
        irrigation_tasks.check_reservoir({'reservoir_ch': '-1'})
        irrigation_tasks.check_reservoir({'reservoir_ch': '3'})

        global _watering_enabled
        # test that _watering_enabled == True if reservoir full
        #irrigation_tasks.check_reservoir({"reservoir_ch"]

        # test that _watering_enabled == False if reservoir empty

if __name__ == '__main__':
    unittest.main()

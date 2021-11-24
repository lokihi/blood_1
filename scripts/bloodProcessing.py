# Подключение функций
import bloodFunctions as s

# Чтение данных
sr_40 = s.file_read("C:\\Users\\Dima\\PycharmProjects\\pythonProject8\\40 mmHg.txt")
sr_60 = s.file_read("C:\\Users\\Dima\\PycharmProjects\\pythonProject8\\60 mmHg.txt")
sr_80 = s.file_read("C:\\Users\\Dima\\PycharmProjects\\pythonProject8\\80 mmHg.txt")
sr_160 = s.file_read("C:\\Users\\Dima\\PycharmProjects\\pythonProject8\\160 mmHg.txt")

# Построение линии тренда
trend = s.calibration(sr_40, sr_60, sr_80, sr_160)

# Построение графиков давления
s.blood_pressure("C:\\Users\\Dima\\PycharmProjects\\pythonProject8\\Calm_mmHg.txt", "calm", trend, "до")
s.blood_pressure("C:\\Users\\Dima\\PycharmProjects\\pythonProject8\\Fitness_mmHg.txt", "fitness", trend, "после")

# Построение графиков пульса
s.pulse("C:\\Users\\Dima\\PycharmProjects\\pythonProject8\\Calm_mmHg.txt", "calm", trend, "до")
s.pulse("C:\\Users\\Dima\\PycharmProjects\\pythonProject8\\Fitness_mmHg.txt", "fitness", trend, "после")

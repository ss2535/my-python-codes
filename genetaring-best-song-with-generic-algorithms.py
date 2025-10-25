# نصب کتابخانه‌های مورد نیاز
!pip install numpy librosa soundfile

import numpy as np
import librosa
import soundfile as sf
import random
from google.colab import drive

# مونت کردن گوگل درایو
drive.mount('/content/drive')

# مسیر پوشه فایل‌های صوتی در گوگل درایو
AUDIO_PATH = '/content/drive/MyDrive/audio_files/'

# نام فایل‌های صوتی
AUDIO_FILES = ['1.wav', '2.wav', '3.wav', '4.wav', '5.wav']

# پارامترهای الگوریتم ژنتیک
POPULATION_SIZE = 20  # اندازه جمعیت
GENOME_LENGTH = 5     # طول هر بردار (۵ بعدی)
GENERATIONS = 10      # تعداد نسل‌ها
MUTATION_RATE = 0.1   # نرخ جهش

# ۱. تولید جمعیت اولیه
def create_population():
    population = []
    for _ in range(POPULATION_SIZE):
        # تولید بردار تصادفی با اعداد ۱ تا ۵
        genome = [random.randint(1, 5) for _ in range(GENOME_LENGTH)]
        population.append(genome)
    return population

# ۲. تابع ارزیابی (Fitness) - اصلاح‌شده
def fitness(genome):
    # بردار ایده‌آل
    ideal = [1, 2, 3, 4, 5]

    # شمارش تعداد تطابق‌ها
    matches = sum(1 for i in range(GENOME_LENGTH) if genome[i] == ideal[i])

    # نگاشت تعداد تطابق‌ها به مقیاس ۱ تا ۵
    fitness_score = 1 + 4 * (matches / GENOME_LENGTH)

    # مطمئن می‌شیم که امتیاز بین ۱ تا ۵ باشه
    fitness_score = max(1, min(5, fitness_score))

    return fitness_score

# ۳. انتخاب والدین (Tournament Selection)
def select_parents(population):
    tournament_size = 3
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=fitness)

# ۴. ترکیب تک‌نقطه‌ای (Crossover)
def crossover(parent1, parent2):
    if random.random() < 0.8:  # احتمال ترکیب
        point = random.randint(1, GENOME_LENGTH - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1, parent2

# ۵. جهش (Mutation)
def mutate(genome):
    for i in range(GENOME_LENGTH):
        if random.random() < MUTATION_RATE:
            genome[i] = random.randint(1, 5)
    return genome

# ۶. ترکیب فایل‌های صوتی بر اساس بهترین بردار
def create_song(best_genome, output_path='output_song.wav'):
    combined_audio = np.array([])
    for gene in best_genome:
        # خواندن فایل صوتی مربوطه
        audio_file = AUDIO_PATH + f'{gene}.wav'
        audio, sr = librosa.load(audio_file, sr=None)
        combined_audio = np.concatenate((combined_audio, audio))

    # ذخیره آهنگ نهایی
    sf.write(output_path, combined_audio, sr)
    print(f"آهنگ نهایی در {output_path} ذخیره شد.")

# الگوریتم ژنتیک اصلی
def genetic_algorithm():
    # تولید جمعیت اولیه
    population = create_population()

    # حلقه اصلی برای تعداد نسل‌ها
    for generation in range(GENERATIONS):
        print(f"نسل {generation + 1}")

        # ارزیابی و مرتب‌سازی جمعیت
        population = sorted(population, key=fitness, reverse=True)

        # ذخیره بهترین بردار
        best_genome = population[0]
        best_fitness = fitness(best_genome)
        print(f"بهترین بردار: {best_genome}, امتیاز: {best_fitness:.4f}")

        # تولید نسل جدید
        new_population = [best_genome]  # حفظ بهترین (Elitism)

        while len(new_population) < POPULATION_SIZE:
            # انتخاب والدین
            parent1 = select_parents(population)
            parent2 = select_parents(population)

            # ترکیب
            child1, child2 = crossover(parent1, parent2)

            # جهش
            child1 = mutate(child1)
            child2 = mutate(child2)

            new_population.append(child1)
            if len(new_population) < POPULATION_SIZE:
                new_population.append(child2)

        population = new_population

    # بهترین بردار نهایی
    best_genome = max(population, key=fitness)
    print(f"\nبهترین آهنگ نهایی: {best_genome}, امتیاز: {fitness(best_genome):.4f}")

    # تولید و ذخیره آهنگ
    create_song(best_genome)

    return best_genome

# اجرای الگوریتم
if name == "__main__":
    random.seed(42)  # برای تکرارپذیری
    genetic_algorithm()
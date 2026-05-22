import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from universities.models import University, Faculty

def seed():
    print("Clearing existing universities and faculties...")
    Faculty.objects.all().delete()
    University.objects.all().delete()

    print("Seeding universities...")
    
    # 1. NUUz
    nuu = University.objects.create(
        name="O'zbekiston Milliy Universiteti (O'zMU)",
        description="O'zbekistonning eng qadimiy va eng yirik oliy ta'lim muassasalaridan biri bo'lib, fundamental fanlar bo'yicha yetakchi hisoblanadi. Talabalarga yuqori darajada nazariy va amaliy bilimlar beriladi.",
        rating=95,
        min_contract=9000000,
        max_contract=15000000,
        website="https://nuu.uz",
        location="tashkent_city",
        university_type="state"
    )
    
    Faculty.objects.create(
        university=nuu,
        name="Amaliy matematika va intellektual tizimlar",
        description="Zamonaviy dasturlash, sun'iy intellekt va ma'lumotlar tahlili (Data Science) yo'nalishida yuqori malakali mutaxassislar tayyorlash.",
        min_score=145.5,
        grant_score=176.8
    )
    Faculty.objects.create(
        university=nuu,
        name="Fizika va astronomiya",
        description="Fundamental va amaliy fizika, yarimo'tkazgichlar fizikasi va kosmik tadqiqotlar bo'yicha ilmiy va akademik yo'nalish.",
        min_score=118.2,
        grant_score=145.0
    )
    Faculty.objects.create(
        university=nuu,
        name="Xorijiy filologiya",
        description="Ingliz, nemis, fransuz va boshqa tillar filologiyasi hamda tarjimonlik mahorati yo'nalishi.",
        min_score=135.7,
        grant_score=165.4
    )

    # 2. TUIT
    tuit = University.objects.create(
        name="Toshkent Axborot Texnologiyalari Universiteti (TATU)",
        description="Axborot texnologiyalari, telekommunikatsiyalar, dasturiy muhandislik va kiberxavfsizlik sohasida Markaziy Osiyodagi eng nufuzli va yetakchi oliygoh.",
        rating=92,
        min_contract=10000000,
        max_contract=18000000,
        website="https://tuit.uz",
        location="tashkent_city",
        university_type="state"
    )
    
    Faculty.objects.create(
        university=tuit,
        name="Dasturiy muhandislik (Software Engineering)",
        description="Yirik dasturiy ta'minot tizimlarini loyihalash, ishlab chiqish va ularni boshqarish bo'yicha professional muhandislarni tayyorlash.",
        min_score=156.3,
        grant_score=182.1
    )
    Faculty.objects.create(
        university=tuit,
        name="Kiberxavfsizlik (Cybersecurity)",
        description="Axborot tizimlari xavfsizligini ta'minlash, tarmoq hujumlarini aniqlash va oldini olish bo'yicha ekspertlarni shakllantirish.",
        min_score=160.9,
        grant_score=185.5
    )
    Faculty.objects.create(
        university=tuit,
        name="Sun'iy intellekt (Artificial Intelligence)",
        description="Mashinali o'qitish, chuqur o'rganish va neyron tarmoqlar texnologiyalarini rivojlantirish.",
        min_score=150.6,
        grant_score=178.3
    )

    # 3. TSTU
    tstu = University.objects.create(
        name="Toshkent Davlat Texnika Universiteti (TDTU)",
        description="Islom Karimov nomidagi Toshkent Davlat Texnika Universiteti muhandislik va texnik fanlar sohasidagi eng yirik va eng qadimiy universitetlardan biridir.",
        rating=85,
        min_contract=8500000,
        max_contract=13000000,
        website="https://tdtu.uz",
        location="tashkent_city",
        university_type="state"
    )
    
    Faculty.objects.create(
        university=tstu,
        name="Mashinasozlik texnologiyalari",
        description="Zamonaviy mashinasozlik sanoati, avtomatlashtirilgan ishlab chiqarish va robototexnika majmualari yo'nalishi.",
        min_score=95,
        grant_score=125
    )
    Faculty.objects.create(
        university=tstu,
        name="Energetika va muhandislik tizimlari",
        description="Issiqlik energetikasi, elektr tarmoqlari va qayta tiklanuvchi energiya manbalari tizimlari loyihasi.",
        min_score=92,
        grant_score=120
    )

    # 4. SamDU
    samdu = University.objects.create(
        name="Samarqand Davlat Universiteti (SamDU)",
        description="Sharaf Rashidov nomidagi Samarqand Davlat Universiteti boy tarixga va nufuzga ega bo'lib, viloyatlardagi eng yirik ta'lim va fan markazlaridan biri hisoblanadi.",
        rating=88,
        min_contract=8000000,
        max_contract=13000000,
        website="https://samdu.uz",
        location="samarkand",
        university_type="state"
    )
    
    Faculty.objects.create(
        university=samdu,
        name="Kimyo va kimyoviy texnologiyalar",
        description="Organik va noorganik kimyo, kimyoviy tahlil hamda sanoat kimyosi yo'nalishi bo'yicha mutaxassislar.",
        min_score=105,
        grant_score=138
    )
    Faculty.objects.create(
        university=samdu,
        name="Tarix va arxeologiya",
        description="Markaziy Osiyo arxeologiyasi va jahon tarixi bo'yicha boy an'analarga ega bo'lgan ilmiy maktab.",
        min_score=110,
        grant_score=142
    )

    # 5. WIUT
    wiut = University.objects.create(
        name="Toshkentdagi Xalqaro Vestminster Universiteti (WIUT)",
        description="Buyuk Britaniyaning Vestminster Universiteti akademik dasturlari asosida dars beruvchi, ingliz tilidagi nufuzli xalqaro oliygoh.",
        rating=96,
        min_contract=32000000,
        max_contract=36000000,
        website="https://wiut.uz",
        location="tashkent_city",
        university_type="private"
    )
    
    Faculty.objects.create(
        university=wiut,
        name="Business Information Systems (BIS)",
        description="Biznes jarayonlarini IT texnologiyalar yordamida optimallashtirish va tizimli tahlil qilish yo'nalishi.",
        min_score=120,
        grant_score=160
    )
    Faculty.objects.create(
        university=wiut,
        name="Economics with Finance",
        description="Iqtisodiy nazariya, moliyaviy bozorlar va investitsion tahlillarni o'rganuvchi yuqori reytingli yo'nalish.",
        min_score=115,
        grant_score=155
    )

    # 6. INHA
    inha = University.objects.create(
        name="Toshkent shahridagi Inha Universiteti (IUT)",
        description="Janubiy Koreyaning INHA universiteti bilan hamkorlikda tashkil etilgan bo'lib, axborot texnologiyalari va logistika sohalarida elita ta'lim beradi.",
        rating=94,
        min_contract=30000000,
        max_contract=32000000,
        website="https://inha.uz",
        location="tashkent_city",
        university_type="private"
    )
    
    Faculty.objects.create(
        university=inha,
        name="Computer Science and Engineering (CSE)",
        description="Dasturlash, algoritmlar, mobil ilovalar va bulutli texnologiyalarni chuqur o'rgatuvchi Koreya andozasidagi dastur.",
        min_score=130,
        grant_score=168
    )
    Faculty.objects.create(
        university=inha,
        name="Business and Logistics (SBL)",
        description="Xalqaro logistika, yuk tashish zanjirlarini boshqarish va global biznes boshqaruvi yo'nalishi.",
        min_score=110,
        grant_score=150
    )

    print(f"Successfully seeded {University.objects.count()} universities and {Faculty.objects.count()} faculties!")

if __name__ == '__main__':
    seed()

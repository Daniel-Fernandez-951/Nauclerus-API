import random

from faker import Faker

# Faker Generator
fake_gen = Faker()
Faker.seed(random.randint(1, 705695))


class LogbookMap:
    def __init__(self):
        self.ac_tail = fake_gen.text(max_nb_chars=20)
        self.ac_mm = fake_gen.text(max_nb_chars=20)
        self.year = fake_gen.text(max_nb_chars=20)
        self.date = fake_gen.text(max_nb_chars=20)
        self.fl_from = fake_gen.text(max_nb_chars=20)
        self.fl_to = fake_gen.text(max_nb_chars=20)
        self.fl_totl = fake_gen.text(max_nb_chars=20)
        self.cat_a_sel = fake_gen.text(max_nb_chars=20)
        self.cat_a_ses = fake_gen.text(max_nb_chars=20)
        self.cat_a_mel = fake_gen.text(max_nb_chars=20)
        self.cat_a_mes = fake_gen.text(max_nb_chars=20)
        self.cat_h = fake_gen.text(max_nb_chars=20)
        self.cat_g = fake_gen.text(max_nb_chars=20)
        self.cat_cstm0 = fake_gen.text(max_nb_chars=20)
        self.cat_cstm1 = fake_gen.text(max_nb_chars=20)
        self.cat_cstm2 = fake_gen.text(max_nb_chars=20)
        self.lndgs_d = fake_gen.text(max_nb_chars=20)
        self.lndgs_n = fake_gen.text(max_nb_chars=20)
        self.cof_n = fake_gen.text(max_nb_chars=20)
        self.cof_inst = fake_gen.text(max_nb_chars=20)
        self.cof_siminst = fake_gen.text(max_nb_chars=20)
        self.cof_app_n = fake_gen.text(max_nb_chars=20)
        self.cof_app_typ = fake_gen.text(max_nb_chars=20)
        self.flight_sim = fake_gen.text(max_nb_chars=20)
        self.tpt_cc = fake_gen.text(max_nb_chars=20)
        self.tpt_solo = fake_gen.text(max_nb_chars=20)
        self.tpt_pic = fake_gen.text(max_nb_chars=20)
        self.tpt_sic = fake_gen.text(max_nb_chars=20)
        self.tpt_dual = fake_gen.text(max_nb_chars=20)
        self.tpt_cfi = fake_gen.text(max_nb_chars=20)
        self.notes = fake_gen.text(max_nb_chars=20)


class NewLogbook:
    def __init__(self):
        self.pilot_id = "overridden"
        self.logbook_style = fake_gen.text(max_nb_chars=20)
        self.header_titles = LogbookMap().__dict__


class LoadedPilot:
    def __init__(self):
        self.email = fake_gen.email()
        self.name = fake_gen.name()
        self.password = fake_gen.password(length=random.randint(128, 256))


class BasicPilot:
    def __init__(self):
        self.email = fake_gen.email()
        self.name = fake_gen.name()
        self.password = fake_gen.password()

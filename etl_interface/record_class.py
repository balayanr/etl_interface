import utils
import definitions
from scipy import misc


# Defines a generic Record class used to store all shared between all records
class Record:
    def __init__(self, image, character, shape, formatting, db, code, code_type):
        self.image = image
        self.character = character
        self.dimensions = shape
        self.format = formatting
        self.database = db
        self.code = code
        self.code_type = code_type

    #getters
    def get_character(self):
        return self.character

    def get_dim(self):
        return self.dimensions

    def get_image(self, reshape = False):
        return self.image.reshape(self.get_dim()) if reshape else self.image

    def get_code(self):
        return self.code

    def get_code_type(self):
        return self.code_type

    # Displays the image in the record
    def display_img(self):
        misc.imshow(self.get_image(reshape=True))

    def save_img(self, filename):
        misc.imsave(filename, self.get_image(reshape=True))


# http://etlcdb.db.aist.go.jp/etlcdb/etln/form_m.htm
class RecordM(Record):
    def __init__(self, data, database):
        Record.__init__(self, image = utils.decode_image(data[32:2048], 4),
                              character = ''.join([chr(x) for x in data[2:4]]),
                              shape = (63,64),
                              formatting = "M",
                              db = database,
                              code = data[6],
                              code_type = "JIS X 0201")
        self.data_number = utils.join_bits(data[0:2], 8)
        self.sheet = utils.join_bits(data[4:6], 8)
        self.ebcdic = data[7]
        self.eval_img = data[8]
        self.eval_group = data[9]
        self.gender = "male" if data[10] == 1 else "female"
        self.age = data[11]
        self.serial_data = utils.join_bits(data[12:16], 8)
        self.ind = utils.join_bits(data[16:18], 8)
        self.occ = utils.join_bits(data[18:20], 8)
        self.sheet_date = data[20:22]
        self.scan_date = data[22:24]
        self.sample_y = data[24]
        self.sample_x = data[25]
        self.min_lvl = data[26]
        self.max_lvl = data[27]

    # Getters
    def get_data_number(self):
        return self.data_number
    def get_sheet(self):
        return self.sheet
    def get_ebcdic(self):
        return self.ebcdic
    def get_eval_img(self):
        return self.eval_img
    def get_eval_group(self):
        return self.eval_group
    def get_gender(self):
        return self.gender
    def get_age(self):
        return self.age
    def get_serial_data(self):
        return self.serial_data
    def get_ind(self):
        return self.ind
    def get_occ(self):
        return self.occ
    def get_sheet_date(self):
        return self.sheet_date
    def get_scan_date(self):
        return self.scan_date
    def get_sample_y(self):
        return self.sample_y
    def get_sample_x(self):
        return self.sample_x
    def get_min_lvl(self):
        return self.min_lvl
    def get_max_lvl(self):
        return self.max_lvl


# http://etlcdb.db.aist.go.jp/etlcdb/etln/form_k.htm
class RecordK(Record):
    def __init__(self, data, database):
        data = utils.decode_record(data)
        Record.__init__(self, image = data[60:3660] * definitions.conversion_factor[6],
                              character = utils.decode_t56code(data[12:18]),
                              shape = (60,60),
                              formatting = "K",
                              db = database,
                              code = bin(utils.join_bits(data[29:31], 6)),
                              code_type = "CO-59 Code")
        self.data_number = utils.join_bits(data[0:6], 6)
        self.mark_style = utils.decode_t56code([data[6]])
        self.style = utils.decode_t56code(data[18:24])

    # Getters
    def get_data_number(self):
        return self.data_number
    def get_mark_style(self):
        return self.mark_style
    def get_style(self):
        return self.style


# http://etlcdb.db.aist.go.jp/etlcdb/etln/form_c.htm
class RecordC(Record):
    def __init__(self, data, database):
        image = data[216:216+2736] #magic numbers from the reference
        data = utils.decode_record(data)
        Record.__init__(self, image = utils.decode_image(image, 4),
                              character = utils.decode_t56code(data[24:28]),
                              shape = (76,72),
                              formatting = "C",
                              db = database,
                              code =  utils.join_bits(data[12:14], 6)>> 4,
                              code_type = "JIS X 0201")
        self.data_number = utils.join_bits(data[0:6], 6)
        self.sheet = utils.join_bits(data[6:12], 6)
        self.ebcdic = utils.join_bits(data[18:24], 6)
        self.eval_img = utils.join_bits(data[30:36], 6)
        self.eval_group = utils.join_bits(data[36:42], 6)
        self.sample_y = utils.join_bits(data[42:48], 6)
        self.sample_x = utils.join_bits(data[48:54], 6)
        self.gender = "male" if utils.join_bits(data[54:60], 6) == 1 else "female"
        self.age = utils.join_bits(data[62:68], 6)
        self.ind = utils.join_bits(data[72:78], 6)
        self.occ = utils.join_bits(data[78:84], 6)
        self.sheet_date = data[84:90]
        self.scan_data = data[90:96]
        self.num_x = utils.join_bits(data[96:102], 6)
        self.num_y = utils.join_bits(data[102:108], 6)
        self.num_lvls = utils.join_bits(data[108:114], 6)
        self.magnification = utils.join_bits(data[114:120], 6)
        self.data_number_old = utils.join_bits(data[120:126], 6)

    # Getters
    def get_data_number(self):
        return self.data_number
    def get_sheet(self):
        return self.sheet
    def get_ebcdic(self):
        return self.ebcdic
    def get_eval_img(self):
        return self.eval_img
    def get_eval_group(self):
        return self.eval_group
    def get_sample_y(self):
        return self.sample_y
    def get_sample_x(self):
        return self.sample_x
    def get_gender(self):
        return self.gender
    def get_age(self):
        return self.age
    def get_ind(self):
        return self.ind
    def get_occ(self):
        return self.occ
    def get_sheet_date(self):
        return self.sheet_date
    def get_scan_date(self):
        return self.scan_date
    def get_num_x(self):
        return self.num_x
    def get_num_y(self):
        return self.num_y
    def get_num_lvl(self):
        return self.num_lvls
    def get_magnification(self):
        return self.magnification
    def get_data_number_old(self):
        return self.data_number_old


# http://etlcdb.db.aist.go.jp/etlcdb/etln/form_e8b.htm
class Record8B(Record):
    def __init__(self, data, database):
        Record.__init__(self, image = utils.decode_image(data[8:512],1),
                              character = ''.join([chr(x) for x in data[4:8]]),
                              shape = (63,64),
                              formatting = "8B",
                              db = database,
                              code =  utils.convert_jis208(data[2:4]),
                              code_type = "JIS X 0208")
        self.sheet = utils.join_bits(data[0:2], 8)

    # Getters
    def get_sheet(self):
        return self.sheet


# http://etlcdb.db.aist.go.jp/etlcdb/etln/form_e8g.htm
class Record8G(Record):
    def __init__(self, data, database):
        self.jisstuff = [data[2:4], utils.join_bits(data[2:4], 8)]
        Record.__init__(self, image = utils.decode_image(data[60:8188], 4),
                              character = ''.join([chr(x) for x in data[4:12]]),
                              shape = (127,128),
                              formatting = "8G",
                              db = database,
                              code = utils.convert_jis208(data[2:4]),
                              code_type = "JIS X 0208")
        self.sheet = utils.join_bits(data[0:2], 8)
        self.data_number = utils.join_bits(data[12:16], 8)
        self.eval_img = data[16]
        self.eval_group = data[17]
        self.gender = "male" if data[18] == 1 else "female"
        self.age = data[19]
        self.ind = utils.join_bits(data[20:22], 8)
        self.occ = utils.join_bits(data[22:24], 8)
        self.sheet_date = utils.join_bits(data[24:26], 8)
        self.scan_date = data[26:28] #YYMM
        self.sample_y = data[28]
        self.sample_x = data[29]

    # Getters
    def get_sheet(self):
        return self.sheet
    def get_data_number(self):
        return self.data_number
    def get_eval_img(self):
        return self.eval_img
    def get_eval_group(self):
        return self.eval_group
    def get_gender(self):
        return self.gender
    def get_age(self):
        return self.age
    def get_ind(self):
        return self.ind
    def get_occ(self):
        return self.occ
    def get_sheet_date(self):
        return self.sheet_date
    def get_scan_date(self):
        return self.scan_date
    def get_sample_y(self):
        return self.sample_y
    def get_sample_x(self):
        return self.sample_x


# http://etlcdb.db.aist.go.jp/etlcdb/etln/form_e9b.htm
class Record9B(Record):
    def __init__(self, data, database):
        Record.__init__(self, image = utils.decode_image(data[8:512],1),
                              character = ''.join([chr(x) for x in data[4:8]]),
                              shape = (63,64),
                              formatting = "9B",
                              db = database,
                              code = utils.convert_jis208(data[2:4]),
                              code_type = "JIS X 0208")
        self.sheet = utils.join_bits(data[0:1], 8)

    # Getters
    def get_sheet(self):
        return self.sheet


# http://etlcdb.db.aist.go.jp/etlcdb/etln/form_e9g.htm
class Record9G(Record):
    def __init__(self, data, database):
        Record.__init__(self, image = utils.decode_image(data[60:8188], 4),
                              character = ''.join([chr(x) for x in data[4:12]]),
                              shape = (127,128),
                              formatting = "8G",
                              db = database,
                              code = utils.convert_jis208(data[2:4]),
                              code_type = "JIS X 0208")
        self.sheet = utils.join_bits(data[0:2], 8)
        self.data_number = utils.join_bits(data[12:16], 8)
        self.eval_img = data[16]
        self.eval_group = data[17]
        self.gender = "male" if data[18] == 1 else "female"
        self.age = data[19]
        self.ind = utils.join_bits(data[20,22], 8)
        self.occ = utils.join_bits(data[22,24], 8)
        self.sheet_date = utils.join_bits(data[24,26], 8)
        self.scan_date = data[26:28] #YYMM
        self.sample_y = data[28]
        self.sample_x = data[29]

    # Getters
    def get_sheet(self):
        return self.sheet
    def get_data_number(self):
        return self.data_number
    def get_eval_img(self):
        return self.eval_img
    def get_eval_group(self):
        return self.eval_group
    def get_gender(self):
        return self.gender
    def get_age(self):
        return self.age
    def get_ind(self):
        return self.ind
    def get_occ(self):
        return self.occ
    def get_sheet_date(self):
        return self.sheet_date
    def get_scan_date(self):
        return self.scan_date
    def get_sample_y(self):
        return self.sample_y
    def get_sample_x(self):
        return self.sample_x


format_to_class = {"M":RecordM,
                   "K":RecordK,
                   "C":RecordC,
                   "8B":Record8B,
                   "8G":Record8G,
                   "9B":Record9B,
                   "9G":Record9G}

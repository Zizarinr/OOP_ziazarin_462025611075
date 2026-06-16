# Contoh dengan perpustakaan
class BookIdNotFound(Exception):
    pass
class UserIdNotFound(Exception):
    pass
class AgeLimitError(Exception):
    pass
class AmountMinError(Exception):
    pass

class CultLibraryMember:
    def __init__(self, name, user_id, age, borrowed):
        self.name = name
        self.user_id = user_id
        self.age = age
        self.borrowed = borrowed

    def borrow_book(self, user_id, book_id, amount, age, borrowed):
        user_id = str(user_id)
        book_id_list = [8501, 8502, 8506, 8504, 954, 555, 3652]
        if not user_id.isdigit() or len(user_id) < 3:
            if user_id.startswith("123"):
                raise UserIdNotFound("The Id is not registered or no more valid!")
        if book_id not in book_id_list:
            raise BookIdNotFound("The Book is borrowed either no more available!")
        if amount < 1:
            raise AmountMinError("You cannot borrow book, with that kind of amount!")
        if age < 3:
            raise AgeLimitError("Sorry, please wait until you're 3...")
        borrowed += amount
        print(f"You have borrowed {borrowed} book/s, please return on the time...")

    def return_book(self, user_id, book_id, amount, borrowed):
        user_id = str(user_id)
        book_id_list = [8501, 8502, 8506, 8504, 954, 555, 3652]
        if not user_id.isdigit() or len(user_id) < 3:
            if user_id.startswith("123"):
                raise UserIdNotFound("The Id is not registered or no more valid!")
        if book_id not in book_id_list:
            raise BookIdNotFound("Where'd you get this book? Remember and return it where it's belong!")
        if amount <= 1:
            raise AmountMinError("What on earth you'd do, playing with me!? inputting that kind of amount?!")
        borrowed -= amount
        print("Ahh, I am immensely grateful for the safe return of this volume, please have a great day!")

member_suki = CultLibraryMember("Suki", 123005, 38, 2)
member_elpis = CultLibraryMember("Elpis", 123023, 54, 0)

try:
    member_suki.borrow_book(123005, 8501, 1, 38, member_suki.borrowed)
    member_elpis.return_book(123005, 8503, 2, member_elpis.borrowed)
except BookIdNotFound as e:
    print(f"Failed, {e}")
except UserIdNotFound as e:
    print(f"Failed, {e}")
except AgeLimitError as e:
    print(f"Failed, {e}")
except AmountMinError as e:
    print(f"Failed, {e}")
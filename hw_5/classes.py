class Client:
    def __init__(
            self,
            first_name: str,
            last_name: str,
            e_mail: str,
            phones=None,
            client_id=None,
    ):
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.e_mail = e_mail
        if phones:
            self.phones = phones.replace(" ", "").split(",")
        else:
            self.phones = []

    def __str__(self):
        return (f"Id: {self.client_id} name: {self.first_name} "
                f"{self.last_name} e-mail: {self.e_mail} "
                f"phones: {', '.join(self.phones) or 'unknown'}")

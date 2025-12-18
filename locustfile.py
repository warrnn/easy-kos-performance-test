from locust import HttpUser, task, between
import re


class BaseUser(HttpUser):
    abstract = True
    host = "http://127.0.0.1:8000"
    # wait_time = between(1, 3)

    username = None
    password = None

    def on_start(self):
        self.login()

    def login(self):
        response = self.client.get("/authentication/login")

        token = re.search(r'name="_token"\s+value="(.+?)"', response.text)

        if not token:
            return

        self.client.post(
            "/authentication/login",
            data={
                "_token": token.group(1),
                "username": self.username,
                "password": self.password,
            },
            allow_redirects=False,
        )
        
        print(token.group(1), self.username, self.password)
        print(response.status_code, response.headers.get("Location"))


class AdminUser(BaseUser):
    # weight = 1
    username = "admin"
    password = "admin"

    @task
    def admin_dashboard(self):
        self.client.get("/admin")

    @task
    def admin_manage_users(self):
        self.client.get("/admin/manage-users")


class PemilikUser(BaseUser):
    # weight = 2
    username = "adit"
    password = "1234"

    @task
    def pemilik_dashboard(self):
        self.client.get("/pemilik_kos/index")

    @task
    def pemilik_laporan(self):
        self.client.get("/pemilik_kos/laporan")


class PenghuniUser(BaseUser):
    # weight = 5
    username = "budi"
    password = "1234"

    @task
    def lihat_kos(self):
        self.client.get("/penghuni/index")

    @task
    def lihat_kamar(self):
        self.client.get("/penghuni/kos/index")

    @task
    def lihat_riwayat_pemesanan(self):
        self.client.get("/penghuni/pemesanan/index")

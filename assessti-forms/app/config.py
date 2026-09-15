from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_credentials_file: str = "/app/credentials/credentials.json"
    # Chave usada para gerar os links de todos os clientes/módulos (auth.py).
    # Compartilhada entre clientes — o token já inclui o slug do cliente na
    # mensagem assinada, então um token de um cliente nunca vale para outro.
    # Trocar invalida TODOS os links já distribuídos, de todos os clientes.
    secret_key: str = "troque-esta-chave-no-.env"

    # PIN de acesso interno da equipe (não confundir com o token por
    # módulo/cliente) — gate único, compartilhado entre todos os clientes,
    # pra abrir a ferramenta de preenchimento ao vivo. Ver pin_auth.py.
    internal_pin: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

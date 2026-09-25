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

    # PIN da página oculta de gestão de leads (/assessment/leads/crm) —
    # gate separado do internal_pin acima (público-alvo e equipe diferentes:
    # comercial vs. quem preenche assessments). Ver leads_crm_auth.py.
    leads_crm_pin: str = "2424"

    # Notificação por e-mail a cada novo lead — Gmail SMTP com senha de app
    # (myaccount.google.com/apppasswords, exige verificação em 2 etapas).
    # Se GMAIL_USER/GMAIL_APP_PASSWORD não estiverem setados, a notificação
    # é só pulada (logada como aviso) — o lead ainda é salvo normalmente,
    # a planilha é a fonte de verdade, o e-mail é só um aviso a mais.
    gmail_user: str = ""
    gmail_app_password: str = ""
    # Destino da notificação — se vazio, usa o próprio gmail_user.
    leads_notify_email: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

def get_pay_text(lang: str):
    texts = {
        "en": "Pay",
        "ru": "Заплатить",
        "by": "Заплаціць",
        "uk": "Заплативши",
        "tr": "Ödemek",
        "de": "Bezahlen",
        "ar": "الدفع",
        "uz": "Тўлаш"
    }
    return texts.get(lang, texts.get("en"))

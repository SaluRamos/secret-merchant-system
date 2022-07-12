class Vars:

    encryption_key = ""
    products = {}
    trades = []
    payment_methods = ["dinheiro", "pix", "dinheiro e pix", "débito", "crédito", "fiado", "consumo", "desconhecido", "perdido/roubado", "agrado/presente"]
    sleeping_time = 0
    max_sleep_time = 180
    min_insight_valid_qtd_qtd = 3
    custom_profit_days = 0
    next_trade_id = 0
    months_to_number = {'jan':1, 'janeiro':1, 'feb':2, 'fev':2, 'fevereiro':2, 'mar':3, 'março':3, 'apr':4, 'abr':4, 'abril':4, 'may':5, 'mai':5, 'maio':5, 'jun':6, 'junho':6, 'jul':7, 'julho':7, 'aug':8, 'ago':8, 'agosto':8, 'sep':9, 'set':9, 'setembro':9, 'oct':10, 'out':10, 'outubro':10, 'nov':11, 'novembro':11, 'dec':12, 'dez':12, 'dezembro':12}
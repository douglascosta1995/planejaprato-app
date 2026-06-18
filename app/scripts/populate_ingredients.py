from app.database.database import SessionLocal
from app.models.ingredient import Ingredient

COMMON_INGREDIENTS = {
    "Grãos e Cereais": [
        "Arroz",
        "Arroz Integral",
        "Feijão Carioca",
        "Feijão Preto",
        "Feijão Branco",
        "Lentilha",
        "Grão-de-Bico",
        "Ervilha",
        "Milho",
        "Aveia",
        "Quinoa",
        "Macarrão",
        "Macarrão Integral",
        "Farinha de Trigo",
        "Farinha de Mandioca",
        "Fubá",
        "Polvilho Doce",
        "Polvilho Azedo",
        "Cuscuz",
        "Pão Francês"
    ],

    "Carnes e Proteínas": [
        "Peito de Frango",
        "Coxa de Frango",
        "Sobrecoxa de Frango",
        "Frango Desfiado",
        "Carne Moída",
        "Patinho",
        "Acém",
        "Alcatra",
        "Contrafilé",
        "Picanha",
        "Costela Bovina",
        "Lombo Suíno",
        "Bacon",
        "Linguiça Calabresa",
        "Presunto",
        "Peito de Peru",
        "Atum",
        "Sardinha",
        "Tilápia",
        "Ovo"
    ],

    "Laticínios": [
        "Leite",
        "Leite Desnatado",
        "Leite Integral",
        "Creme de Leite",
        "Leite Condensado",
        "Iogurte Natural",
        "Iogurte Grego",
        "Manteiga",
        "Margarina",
        "Requeijão",
        "Queijo Mussarela",
        "Queijo Prato",
        "Queijo Minas",
        "Queijo Parmesão",
        "Ricota"
    ],

    "Legumes": [
        "Batata",
        "Batata Doce",
        "Mandioca",
        "Mandioquinha",
        "Inhame",
        "Cenoura",
        "Beterraba",
        "Abobrinha",
        "Berinjela",
        "Chuchu",
        "Abóbora",
        "Pepino",
        "Vagem",
        "Quiabo",
        "Jiló"
    ],

    "Verduras e Folhas": [
        "Alface",
        "Alface Americana",
        "Rúcula",
        "Agrião",
        "Couve",
        "Couve-Flor",
        "Brócolis",
        "Espinafre",
        "Repolho",
        "Acelga",
        "Salsinha",
        "Cebolinha",
        "Coentro"
    ],

    "Frutas": [
        "Banana",
        "Maçã",
        "Laranja",
        "Limão",
        "Mamão",
        "Abacaxi",
        "Manga",
        "Melancia",
        "Melão",
        "Morango",
        "Uva",
        "Pera",
        "Kiwi",
        "Abacate",
        "Maracujá"
    ],

    "Temperos e Condimentos": [
        "Alho",
        "Cebola",
        "Tomate",
        "Extrato de Tomate",
        "Molho de Tomate",
        "Sal",
        "Pimenta-do-Reino",
        "Páprica",
        "Orégano",
        "Cominho",
        "Colorau",
        "Açafrão",
        "Mostarda",
        "Ketchup",
        "Maionese",
        "Vinagre",
        "Azeite de Oliva",
        "Óleo de Soja",
        "Molho Shoyu"
    ],

    "Doces e Panificação": [
        "Açúcar",
        "Açúcar Mascavo",
        "Chocolate em Pó",
        "Achocolatado",
        "Fermento Químico",
        "Fermento Biológico",
        "Leite de Coco",
        "Coco Ralado",
        "Baunilha",
        "Mel"
    ]
}

db = SessionLocal()

count = 0

for category, ingredients in COMMON_INGREDIENTS.items():
    for ingredient_name in ingredients:

        exists = (
            db.query(Ingredient)
            .filter(Ingredient.name == ingredient_name)
            .first()
        )

        if not exists:
            db.add(
                Ingredient(
                    name=ingredient_name
                )
            )
            count += 1

db.commit()

print(f"{count} ingredientes adicionados.")

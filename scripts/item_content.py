import turicreate as tc

# Cargamos los datos recogidos en la web
actions = tc.SFrame.read_csv('../Datasets/favorites.csv')

# Creamos los juegos de datos para entrenamiento y validación
training_data, validation_data = tc.recommender.util.random_split_by_user(actions, 'user_id', 'show_id')

# Suponemos que el archivo favorites.csv tiene una columna extra llama ratings
model = tc.item_content_recommender.create(training_data,
                        user_id='user_id',
                        item_id='show_id')

recommendations = model.get_similar_items()

# Vamos a suponer que hemos terminado de ver Stranger Things (66732) y
# queremos recomendar al usuario otros shows parecidos a este en base
# a su lista de preferencias

shows = tc.SFrame.read_csv('../Datasets/shows.csv')
(recommendations[(recommendations['show_id'] == 66732)]).join(right=shows,on={'similar':'show_id'},how='inner').sort('rank', ascending=True).print_rows()

model.export_coreml("../Models/MyItemContentRecommender.mlmodel")                                             
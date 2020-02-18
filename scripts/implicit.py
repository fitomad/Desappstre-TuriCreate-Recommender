import turicreate as tc

# Cargamos los datos recogidos en la web
actions = tc.SFrame.read_csv('../Datasets/favorites.csv')

# Creamos los juegos de datos para entrenamiento y validación
training_data, validation_data = tc.recommender.util.random_split_by_user(actions, 'user_id', 'show_id')

# Creamos el modelo
model = tc.recommender.item_similarity_recommender.create(training_data,
                                          user_id='user_id',
                                          item_id='show_id')


# Series similares a Stranger Things
recommendations = model.get_similar_items(items=[ 66732 ])

# Para saber el nombre de las series hacemos un join con el SFrame d
# que contiene los datos de los shows.
# Esto no afecta al modelo en modo alguno.
shows = tc.SFrame.read_csv('../Datasets/shows.csv')
recommendations.join(right=shows,on={'similar':'show_id'},how='inner').sort('rank', ascending=True).print_rows()

model.export_coreml("../Models/MyImplicitRecommender.mlmodel")                                          
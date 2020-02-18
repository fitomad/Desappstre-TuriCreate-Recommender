import turicreate as tc

# Cargamos los datos recogidos en la web
actions = tc.SFrame.read_csv('../Datasets/favorites-rating.csv')
shows = tc.SFrame.read_csv('../Datasets/shows.csv')

# Creamos los juegos de datos para entrenamiento y validación
training_data, validation_data = tc.recommender.util.random_split_by_user(actions, 'user_id', 'show_id')

# Creamos el modelo junto con la Side Information
model = tc.ranking_factorization_recommender.create(training_data,
                        item_data=shows,
                        user_id='user_id',
                        item_id='show_id',
                        target='rating',
                        binary_target=True)

recommendations = model.recommend(users=['c5d83985-6060-4fd5-8079-7acea3cdc67a'])

# recomendaciones por si te ha gustado un show en concreto
recommendations.print_rows()

model.export_coreml("../Models/MyExplicitRecommender.mlmodel")                                             
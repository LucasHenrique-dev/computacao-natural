import optuna
from optuna.visualization import plot_pareto_front

from aco import ACO_VRP
from rotas import Route


def algoritmo(parametro_1, parametro_2, parametro_3):
    objetivo_1 = parametro_1**2 + parametro_2**2
    objetivo_2 = parametro_3 - parametro_2 + parametro_1
    return objetivo_1, objetivo_2


def execute(parametro_1, parametro_2, parametro_3):
    # Aqui você pode fazer algum processamento ou algo caso se faça necessario
    return algoritmo(parametro_1, parametro_2, parametro_3)


def objective(trial):
    # Definir os parâmetros que você precisa controlar (o range e os tipos)
    parametro_1 = trial.suggest_int('parametro_1', -10, 10)
    parametro_2 = trial.suggest_categorical('parametro_2', [0, 3, 5, 10, -8])
    parametro_3 = trial.suggest_float('parametro_3', 0.25, 0.888)

    return execute(parametro_1, parametro_2, parametro_3)


def execute2(parametro_1, parametro_2, parametro_3, parametro_4):
    routes = Route(17, 12, min_deposit_coord=10, max_deposit_coord=50)
    routes.create_routes()
    aco = ACO_VRP(routes, 12, num_ants=20, num_iterations=300, max_stagnation=20,
                  alpha=parametro_1, beta=parametro_2, rho=parametro_3, Q=parametro_4)
    _, best_cost = aco.run()

    return best_cost


def objective2(trial):
    # Definir os parâmetros que você precisa controlar (o range e os tipos)
    # Parametros: alpha=1.0, beta=2.0, rho=0.5, Q=10
    parametro_1 = trial.suggest_float('parametro_1', 1.0, 2.0)
    parametro_2 = trial.suggest_float('parametro_2', 1.0, 2.0)
    parametro_3 = trial.suggest_float('parametro_3', 0.2, 0.8)
    parametro_4 = trial.suggest_int('parametro_4', 1, 10)

    return execute2(parametro_1, parametro_2, parametro_3, parametro_4)


if __name__ == '__main__':
    # Aqui você cria seu teste e define se cada objetivo é de maximização ou minimização
    study1 = optuna.create_study(directions=["maximize", "minimize"])
    study2 = optuna.create_study(directions=["minimize"])

    # Tempo Limite
    um_dia = 86400
    # Defini como 12s
    timelimit = um_dia/7200

    # study1.optimize(objective, timeout=timelimit, n_jobs=1)
    # print(study1.best_trials[-1])

    # Gera o pareto front
    # plot_pareto_front(study1)

    study2.optimize(objective2, timeout=60, n_jobs=1)
    print(study2.best_params)

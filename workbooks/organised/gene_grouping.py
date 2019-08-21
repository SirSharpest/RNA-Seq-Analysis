from sklearn.gaussian_process import GaussianProcessRegressor

import numpy as np


def fold(a, b):
    c = np.empty((a.flatten().size + b.flatten().size),
                 dtype=a.flatten().dtype)
    c[0::2] = a.flatten()
    c[1::2] = b.flatten()
    return c


def stretch(a): return a.reshape(len(a), 1)


def scaler_for_genes(a):
    b = a/a[0]
    return b


def generate_estimations_for_profile_compare(a, b):
    a = a.astype('float64').flatten()
    b = b.astype('float64').flatten()
    a = scaler_for_genes(a)
    b = scaler_for_genes(b)

    c = fold(a, b)
    t_a = np.arange(len(a.flatten()))
    t_c = fold(t_a, t_a)

    model_a = GaussianProcessRegressor().fit(stretch(t_a), stretch(a))
    model_b = GaussianProcessRegressor().fit(stretch(t_a), stretch(b))
    model_c = GaussianProcessRegressor().fit(stretch(t_c), stretch(c))

    y_hat_a = model_a.predict(stretch(t_a))
    y_hat_b = model_b.predict(stretch(t_a))
    y_hat_c = model_c.predict(stretch(t_c))

    return (y_hat_a, y_hat_b, y_hat_c, t_a, t_c, c, a, b)


def is_one_model_best(a, b, print_scores=False):
    y_hat_a, y_hat_b, y_hat_c, y_a, y_c, c, a, b = generate_estimations_for_profile_compare(
        a, b)

    def aic_1var(y, y_hat): return 2 + len(y.flatten()) * \
        np.log(np.sum((y.flatten() - y_hat.flatten())**2))

    def aic_2var(y1, y1_hat, y2, y2_hat): return 2*2 + len(y1.flatten()) + len(y2.flatten()) * \
        np.log(np.sum([(y1.flatten() - y1_hat.flatten()) **
                       2, (y2.flatten() - y2_hat.flatten())**2]))

    aic_ab = aic_2var(a, y_hat_a, b, y_hat_b)
    aic_c = aic_1var(c, y_hat_c)

    if print_scores:
        print('SSE A+B:', aic_ab)
        print('SSE C:  ', aic_c)
    if aic_c < aic_ab:
        return True
    return False


np.random.seed(42)
groups = {}
matches = {}
genes = {"gene_{0}".format(k): v+0.1 for k,
         v in enumerate(np.around(np.random.rand(100, 3), 1))}
for g in genes.values():
    g[0] = 0.1
#genes['test_g'] = genes['gene_0']

for g1, x1 in genes.items():
    for g2, x2 in genes.items():
        if g1 == g2:
            continue
        if is_one_model_best(x1, x2):

            if g1 in matches or g2 in matches:
                if g1 in matches:
                    if g2 in matches[g1]:
                        continue
                    matches[g1].append(g2)
                    print("{0} and {1} are a match".format(g1, g2))
                if g2 in matches:
                    if g1 in matches[g2]:
                        continue
                    matches[g2].append(g1)
                    print("{0} and {1} are a match".format(g1, g2))
            else:
                matches[g1] = [g2]
                print("{0} and {1} are a match".format(g1, g2))

genes_as_lists = []

for k, v in matches.items():
    genes_as_lists.append(v)
    genes_as_lists[-1].append(k)
#  for k, v in matches.items():
#      plot_models(genes[k],genes[v[0]])

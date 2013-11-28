#include <vector>
#include <iostream>
#include <cmath>
#include <boost/python.hpp>

long double det(long double **sigma, int d) {
    long double r = 1;
    for (int i = 0; i < d; i++)
        r *= sigma[i][i];

    return r;
}

long double calcProduct(long double **sigma, long double *mu, long double* x, int d) {
    long double r = 0;
    for (int i = 0; i < d; i++)
        r += (x[i]-mu[i])*(x[i]-mu[i])/sigma[i][i];

    return r;
}

long double* sumVect(long double *v1, long double *v2, long double a, int d) {
    long double *r = (long double*)malloc(sizeof(long double)*d);
    for (int i = 0; i < d; i++) {
        r[i] = v1[i] + v2[i]*a;
    }

    return r;
}

long double** sumMat(long double **mat, long double *v1, long double *v2, long double a, int d) {
    long double **r = (long double**)malloc(sizeof(long double)*d*d);
    for (int i = 0; i < d; i++) {
        r[i] = (long double*)malloc(sizeof(long double)*d);
        for (int j = 0; j < d; j++) {
            if (i == j)
                r[i][j] = mat[i][j] + (v1[i]-v2[i])*(v1[i]-v2[i])*a;
            else
                r[i][j] = 0;
        }
    }

    return r;
}

long double* mulVect(long double *v, long double a, int d) {
    long double *r = (long double*)malloc(sizeof(long double)*d);
    for (int i = 0; i < d; i++)
        r[i] = v[i]/a;

    return r;
}

long double** mulMat(long double **m, long double a, int d) {
    long double s = 0;
    for (int i = 0; i < d; i++)
        s += m[i][i]/a;

    long double **r = (long double**)malloc(sizeof(long double)*d*d);
    for (int i = 0; i < d; i++) {
        r[i] = (long double*)malloc(sizeof(long double)*d);
        for (int j = 0; j < d; j++) {
            if (i == j) {
                if (m[i][j] <= 0)
                    r[i][j] = s/(d*d);
                else
                    r[i][j] = m[i][j]/a;
            }
            else
                r[i][j] = 0;
        }
    }

    return r;
}

class ContinuousMarkov {
public:
    ContinuousMarkov(int n, int m, int d, long double *PI, long double**A, long double **C, long double ***G_mu, long double ****G_sigma);

    void render();

    long double calcGaussianValue(long double **sigma, long double *mu, long double *x); // Calculates a single probability for a vector x_ in the gaussian sigma
    long double* calcProbabilitiesVector(long double *x); // Calculate a probability for a vector x in each state's mixture
    long double** calcProbabilitiesSequence(long double **seq, int s); // Calculate probabilities for each vector of the sequence seq
    long double** forward(long double **seq, int s, long double **prob, long double *p); // Implementation of the forward algorithm
    long double** backward(long double **seq, int s, long double **prob); // Implementation of the backward algorithm (doesn't return overall probability)
    void calcXiOldGamma(long double **seq, int s, long double **alpha, long double **beta, long double p, long double **prob, long double ***xi, long double **oldGamma); // Calculates Xis and Old Gammas for latter calculus
    long double*** calcGamma(long double **seq, int s, long double **alpha, long double **beta, long double **prob); // Calculates gamma for latter calculus
    void calcSums(long double ***seqs, int sN, int *sS, long double ****gammas, long double **littleSums, long double ***littleVect, long double ****littleMat, long double *fatSums); // Calculates partial sums for latter calculus
    void baumWelch(long double ***seqs, int sN, int *sS, int maxIt = 1, int epsilon = 0.0000000001);

    int n;
    int m;
    int d;
    long double *PI;
    long double **A;
    long double **C;
    long double ***G_mu;
    long double ****G_sigma;
};

ContinuousMarkov::ContinuousMarkov(int n, int m, int d, long double *PI, long double **A, long double **C, long double ***G_mu, long double ****G_sigma) {
    this->n = n;
    this->m = m;
    this->d = d;
    this->PI = PI;
    this->A = A;
    this->C = C;
    this->G_mu = G_mu;
    this->G_sigma = G_sigma;
}

void ContinuousMarkov::render() {
    std::cout << "Markov's Continuous Automat" << std::endl;
    std::cout << "PI : [";
    for (int i = 0; i < n; i++) {
        if (i != n-1)
            std::cout << PI[i] << ", ";
        else
            std::cout << PI[i] << "]" << std::endl << std::endl;
    }

    std::cout << "A : [" << std::endl;
    for (int i = 0; i < n; i++) {
        std::cout << "[";
        for (int j = 0; j < n; j++) {
            if (j != n-1)
                std::cout << A[i][j] << ", ";
            else
                std::cout << A[i][j] << "]" << std::endl;
        }
        if (i == n-1)
            std::cout << "]" << std::endl << std::endl;
    }

    std::cout << "C : [" << std::endl;
    for (int i = 0; i < n; i++) {
        std::cout << "[";
        for (int j = 0; j < m; j++) {
            if (j != m-1)
                std::cout << C[i][j] << ", ";
            else
                std::cout << C[i][j] << "]" << std::endl;
        }
        if (i == n-1)
            std::cout << "]" << std::endl << std::endl;
    }

    std::cout << "G_mu : [" << std::endl;
    for (int i = 0; i < n; i++) {
        std::cout << "[";
        for (int j = 0; j < m; j++) {
            if (j != m-1) {
                std::cout << "[";
                for (int a = 0; a < d; a++)
                    std::cout << G_mu[i][j][a] << ", ";
                std::cout << "]" << std::endl;
            } else {
                std::cout << "[";
                for (int a = 0; a < d; a++)
                    std::cout << G_mu[i][j][a] << ", ";
                std::cout << "]" << std::endl;
                std::cout << "]" << std::endl;
            }
        }
        if (i == n-1)
            std::cout << "]" << std::endl << std::endl;
    }

    std::cout << "G_sigma : [" << std::endl;
    for (int i = 0; i < n; i++) {
        std::cout << "[";
        for (int j = 0; j < m; j++) {
            if (j != m-1) {
                std::cout << "[";
                for (int a = 0; a < d; a++)
                    std::cout << G_sigma[i][j][a][a] << ", ";
                std::cout << "]" << std::endl;
            } else {
                std::cout << "[";
                for (int a = 0; a < d; a++)
                    std::cout << G_sigma[i][j][a][a] << ", ";
                std::cout << "]" << std::endl;
                std::cout << "]" << std::endl;
            }
        }
        if (i == n-1)
            std::cout << "]" << std::endl << std::endl;
    }
}

long double ContinuousMarkov::calcGaussianValue(long double **sigma, long double *mu, long double *x) {
    long double den = sqrt(pow(2*M_PI, d) * det(sigma, d));
    long double num = exp((long double)-.5 * calcProduct(sigma, mu, x, d));

    if (num/den > 1) // Probability over 1, Markov's bullshit continuous theory
        return 1.1;
    else
        return num/den;
}

long double* ContinuousMarkov::calcProbabilitiesVector(long double *x) {
    long double* r = (long double*)malloc(sizeof(long double)*n);
    for (int i = 0; i < n; i++) {
        r[i] = 0;
        for (int j = 0; j < m; j++)
            r[i] += C[i][j]*calcGaussianValue(G_sigma[i][j], G_mu[i][j], x);
    }

    return r;
}

long double** ContinuousMarkov::calcProbabilitiesSequence(long double **seq, int s) {
    long double **r = (long double**)malloc(sizeof(long double)*s*n);
    for (int i = 0; i < s; i++)
        r[i] = calcProbabilitiesVector(seq[i]);

    return r;
}

long double** ContinuousMarkov::forward(long double **seq, int s, long double **prob, long double *p) {
    long double **alpha = (long double**)malloc(sizeof(long double)*s*n);
    for (int t = 0; t < s; t++) // Initialization of the alpha
        alpha[t] = (long double*)malloc(sizeof(long double)*n);
    for (int i = 0; i < n; i++) // Setting for each state value at t=0
        alpha[0][i] = PI[i]*prob[0][i];

    for (int t = 1; t < s; t++) {
        for (int i = 0; i < n; i++) {
            long double r = 0;
            for (int j = 0; j < n; j++)
                r += alpha[t-1][j]*A[j][i];
            alpha[t][i] = r*prob[t][i];
        }
    }

    *p = 0;
    for (int i = 0; i < n; i++)
        *p += alpha[s-1][i];

    return alpha;
}

long double** ContinuousMarkov::backward(long double **seq, int s, long double **prob) {
    long double **beta = (long double**)malloc(sizeof(long double)*s*n);
    for (int t = 0; t < s; t++) // Initialization of the beta
        beta[t] = (long double*)malloc(sizeof(long double)*n);
    for (int i = 0; i < n; i++) // Setting for each state value at t=s-1
        beta[s-1][i] = 1;

    for (int t = s-2; t >= 0; t--) {
        for (int i = 0; i < n; i++) {
            long double r = 0;
            for (int j = 0; j < n; j++)
                r += A[i][j]*beta[t+1][j]*prob[t+1][j];
            beta[t][i] = r;
        }
    }

    return beta;
}

// Uses xi and oldGamma. WARNING : xi and oldGamma must be defined !
void ContinuousMarkov::calcXiOldGamma(long double **seq, int s, long double **alpha, long double **beta, long double p, long double **prob, long double ***xi, long double **oldGamma) {
    for (int t = 0; t < s-1; t++) {
        for (int i = 0; i < n; i++) {
            oldGamma[t][i] = 0;
            for (int j = 0; j < n; j++) {
                xi[t][i][j] = alpha[t][i]*A[i][j]*prob[t+1][j]*beta[t+1][j]/p;
                oldGamma[t][i] += xi[t][i][j];
            }
        }
    }
}

long double*** ContinuousMarkov::calcGamma(long double **seq, int s, long double **alpha, long double **beta, long double **prob) {
    long double ***gamma = (long double***)malloc(sizeof(long double)*s*n*m);
    for (int t = 0; t < s; t++) {
        long double sumAB = 0;
        for (int i = 0; i < n; i++)
            sumAB += alpha[t][i]*beta[t][i];

        gamma[t] = (long double**)malloc(sizeof(long double)*n*m);
        for (int i = 0; i < n; i++) {
            long double AB = alpha[t][i]*beta[t][i]/sumAB;
            gamma[t][i] = (long double*)malloc(sizeof(long double)*m);
            for (int k = 0; k < m; k++) {
                if (prob[t][i] == 0) // This means the sum of probabilities is 0, thus a single one of them will be 0 too
                    gamma[t][i][k] = 0;
                else
                    gamma[t][i][k] = AB*C[i][k]*calcGaussianValue(G_sigma[i][k], G_mu[i][k], seq[t])/prob[t][i];
            }
        }
    }

    return gamma;
}

// Uses littleSums, littleVect, littleMat, fatSums. WARNING : they must be defined !
void ContinuousMarkov::calcSums(long double ***seqs, int sN, int *sS, long double ****gammas, long double **littleSums, long double ***littleVect, long double ****littleMat, long double *fatSums) {
    for (int i = 0; i < n; i++) {
        fatSums[i] = 0;
        for (int k = 0; k < m; k++) {
            littleSums[i][k] = 0;
            for (int a = 0; a < d; a++) {
                littleVect[i][k][a] = 0;
                for (int b = 0; b < d; b++)
                    littleMat[i][k][a][b] = 0;
            }

            for (int s = 0; s < sN; s++) {
                for (int t = 0; t < sS[s]; t++) {
                    littleSums[i][k] += gammas[s][t][i][k];
                    littleVect[i][k] = sumVect(littleVect[i][k], seqs[s][t], gammas[s][t][i][k], d);
                    littleMat[i][k] = sumMat(littleMat[i][k], seqs[s][t], G_mu[i][k], gammas[s][t][i][k], d);
                }
            }
            fatSums[i] += littleSums[i][k];
        }
    }
}

void ContinuousMarkov::baumWelch(long double ***seqs, int sN, int *sS, int maxIt, int epsilon) {
    long double oldLike = -1;
    int it = 0;
    bool decrease = false;
    int totalSize = 0;
    for (int s = 0; s < sN; s++)
        totalSize += sS[s];

    while (it < maxIt) {
        long double ***alphas = (long double***)malloc(sizeof(long double)*totalSize*n);
        long double ***betas = (long double***)malloc(sizeof(long double)*totalSize*n);
        long double *ps = (long double*)malloc(sizeof(long double)*sN);
        long double ***probs = (long double***)malloc(sizeof(long double)*totalSize*n);

        long double ****xis = (long double****)malloc(sizeof(long double)*totalSize*n*n);
        long double ***oldGammas = (long double***)malloc(sizeof(long double)*totalSize*n);
        long double ****gammas = (long double****)malloc(sizeof(long double)*totalSize*n*n);
        for (int s = 0; s < sN; s++)
            probs[s] = calcProbabilitiesSequence(seqs[s], sS[s]);

        for (int s = 0; s < sN; s++) {
            alphas[s] = forward(seqs[s], sS[s], probs[s], &ps[s]);
            betas[s] = backward(seqs[s], sS[s], probs[s]);

            // Allocation of xis and oldGammas
            xis[s] = (long double***)malloc(sizeof(long double)*sS[s]*n*n);
            oldGammas[s] = (long double**)malloc(sizeof(long double)*sS[s]*n);
            for (int t = 0; t < sS[s]; t++) {
                xis[s][t] = (long double**)malloc(sizeof(long double)*n*n);
                for (int i = 0; i < n; i++)
                    xis[s][t][i] = (long double*)malloc(sizeof(long double)*n);
                oldGammas[s][t] = (long double*)malloc(sizeof(long double)*n);
            }

            calcXiOldGamma(seqs[s], sS[s], alphas[s], betas[s], ps[s], probs[s], xis[s], oldGammas[s]);
            gammas[s] = calcGamma(seqs[s], sS[s], alphas[s], betas[s], probs[s]);
        }

        // Allocation of partial sums
        long double **littleSums = (long double**)malloc(sizeof(long double)*n*m);
        long double ***littleVect = (long double***)malloc(sizeof(long double)*n*m*d);
        long double ****littleMat = (long double****)malloc(sizeof(long double)*n*m*d*d);
        long double *fatSums = (long double*)malloc(sizeof(long double)*n);
        for (int i = 0; i < n; i++) {
            littleSums[i] = (long double*)malloc(sizeof(long double)*m);
            littleVect[i] = (long double**)malloc(sizeof(long double)*m*d);
            littleMat[i] = (long double***)malloc(sizeof(long double)*m*d*d);
            for (int j = 0; j < m; j++) {
                littleVect[i][j] = (long double*)malloc(sizeof(long double)*d);
                littleMat[i][j] = (long double**)malloc(sizeof(long double)*d*d);
                for (int a = 0; a < d; a++)
                    littleMat[i][j][a] = (long double*)malloc(sizeof(long double)*d);
            }
        }
        calcSums(seqs, sN, sS, gammas, littleSums, littleVect, littleMat, fatSums);

        // Allocation of new model parameters
        long double *_PI = (long double*)malloc(sizeof(long double)*n);
        long double **_A = (long double**)malloc(sizeof(long double)*n*n);
        long double **_C = (long double**)malloc(sizeof(long double)*n*m);
        long double ***_G_mu = (long double***)malloc(sizeof(long double)*n*m*d);
        long double ****_G_sigma = (long double****)malloc(sizeof(long double)*n*m*d*d);
        for (int i = 0; i < n; i++) {
            _A[i] = (long double*)malloc(sizeof(long double)*n);
            _C[i] = (long double*)malloc(sizeof(long double)*m);
            _G_mu[i] = (long double**)malloc(sizeof(long double)*m*d);
            _G_sigma[i] = (long double***)malloc(sizeof(long double)*m*d*d);
            for (int j = 0; j < m; j++) {
                _G_mu[i][j] = (long double*)malloc(sizeof(long double)*d);
                _G_sigma[i][j] = (long double**)malloc(sizeof(long double)*d*d);
                for (int a = 0; a < d; a++)
                    _G_sigma[i][j][a] = (long double*)malloc(sizeof(long double)*d);
            }
        }

        long double r = 0;
        long double num = 0;
        long double den = 0;
        for (int i = 0; i < n; i++) {
            // Setting PI and A
            r = 0;
            den = 0;
            for (int s = 0; s < sN; s++) {
                r += oldGammas[s][0][i];
                for (int t = 0; t < sS[s]; t++)
                    den += oldGammas[s][t][i];
            }
            _PI[i] = r/sN;

            if (den == 0) { // This means the probability to be in state i at time t is 0
                // So probabilities to go from i at t to j at t+1 will be 0 for each j
                for (int j = 0; j < n; j++)
                    _A[i][j] = 0;
            }
            else {
                for (int j = 0; j < n; j++) {
                    num = 0;
                    for (int s = 0; s < sN; s++) {
                        for (int t = 0; t < sS[s]; t++)
                            num += xis[s][t][i][j];
                    }
                    _A[i][j] = num/den;
                }
            }

            // Setting C, G_mu and G_sigma
            for (int k = 0; k < m; k++) {
                _C[i][k] = littleSums[i][k]/fatSums[i];
                _G_mu[i][k] = mulVect(littleVect[i][k], littleSums[i][k], d);
                _G_sigma[i][k] = mulMat(littleMat[i][k], littleSums[i][k], d);
            }

        }

        long double like = 1;
        long double mean = 0;
        for (int s = 0; s < sN; s++) {
            like *= ps[s];
            mean += ps[s];
        }

        mean /= sN;
        std::cout << "Likelyhood : " << like << " (" << mean << ")" << std::endl << std::endl;
        long double rap = 1;
        if (oldLike != -1) {
            rap = like/oldLike;
            if (rap < 1) {
                decrease = true;
                break;
            }
            else if (rap < (1+epsilon))
                break;
        }

        oldLike = like;
        PI = _PI;
        A = _A;
        C = _C;
        G_mu = _G_mu;
        G_sigma = _G_sigma;

        it++;
    }

    if (it == maxIt)
        std::cout << "Ended on max iteration" << std::endl;
    else if (decrease)
        std::cout << "Ended on decreasing likelyhood" << std::endl;
    else
        std::cout << "Ended on stationary likelyhod" << std::endl;

    std::cout << "Final likelyhood (iteration " << it << ") : " << oldLike << std::endl;
}

ContinuousMarkov *M = NULL;

void createMarkov(int n, int m, int d, boost::python::list _PI, boost::python::list _A, boost::python::list _C, boost::python::list _G_mu, boost::python::list _G_sigma) {
    long double *PI = (long double*)malloc(sizeof(long double)*n);
    long double **A = (long double**)malloc(sizeof(long double)*n*n);
    long double **C = (long double**)malloc(sizeof(long double)*n*m);
    long double ***G_mu = (long double***)malloc(sizeof(long double)*n*m*d);
    long double ****G_sigma = (long double****)malloc(sizeof(long double)*n*m*d*d);

    for(int i = 0; i < n; i++) {
        PI[i] = boost::python::extract<long double>(_PI[i]);

        A[i] = (long double*)malloc(sizeof(long double)*n);
        for (int j = 0; j < n; j++)
            A[i][j] = boost::python::extract<long double>(_A[i][j]);

        C[i] = (long double*)malloc(sizeof(long double)*m);
        G_mu[i] = (long double**)malloc(sizeof(long double)*m*d);
        G_sigma[i] = (long double***)malloc(sizeof(long double)*m*d*d);
        for (int j = 0; j < m; j++) {

            C[i][j] = boost::python::extract<long double>(_C[i][j]);

            G_mu[i][j] = (long double*)malloc(sizeof(long double)*d);
            G_sigma[i][j] = (long double**)malloc(sizeof(long double)*d*d);
            for (int k = 0; k < d; k++) {
                G_mu[i][j][k] = boost::python::extract<long double>(_G_mu[i][j][k]);

                G_sigma[i][j][k] = (long double*)malloc(sizeof(long double)*d);
                for (int l = 0; l < d; l++)
                    G_sigma[i][j][k][l] = boost::python::extract<long double>(_G_sigma[i][j][k][l]);
            }
        }
    }

    M = new ContinuousMarkov(n, m, d, PI, A, C, G_mu, G_sigma);
}

long double forward(boost::python::list _seq) {
    if (!M)
        return -1;

    int s = boost::python::len(_seq);

    long double **seq = (long double**)malloc(sizeof(long double)*s*M->d);
    for (int t = 0; t < s; t++) {
        seq[t] = (long double*)malloc(sizeof(long double)*M->d);
        for (int i = 0; i < M->d; i++)
            seq[t][i] = boost::python::extract<long double>(_seq[t][i]);
    }

    long double p;
    long double **prob = M->calcProbabilitiesSequence(seq, s);
    M->forward(seq, s, prob, &p);

    return p;
}

void baumWelch(boost::python::list _seqs) {
    if (!M)
        return;

    int sN = boost::python::len(_seqs);

    int *sS = (int*)malloc(sizeof(int)*sN);
    int totalSize = 0;
    for (int s = 0; s < sN; s++) {
        sS[s] = boost::python::len(boost::python::extract<boost::python::list>(_seqs[s]));
        totalSize += sS[s];
    }

    long double ***seqs = (long double***)malloc(sizeof(long double)*totalSize*M->d);
    for (int s = 0; s < sN; s++) {
        seqs[s] = (long double**)malloc(sizeof(long double)*sS[s]*M->d);
        for (int t = 0; t < sS[s]; t++) {
            seqs[s][t] = (long double*)malloc(sizeof(long double)*M->d);
            for (int i = 0; i < M->d; i++)
                seqs[s][t][i] = boost::python::extract<long double>(_seqs[s][t][i]);
        }
    }

    M->baumWelch(seqs, sN, sS);
}

void renderMarkov() {
    if (M)
        M->render();
}

BOOST_PYTHON_MODULE(hmm)
{
    using namespace boost::python;
    def("createMarkov", createMarkov);
    def("renderMarkov", renderMarkov);
    def("forward", forward);
    def("baumWelch", baumWelch);
}

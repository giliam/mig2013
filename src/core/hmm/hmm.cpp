#include <vector>
#include <iostream>
#include <cmath>
#include <string>
#include <boost/python.hpp>

const long double MIN_VALUE = 0.00001;

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

void sumVects(long double ***seqs, long double ****gammas, int d, int sN, int *sS, int i, int k, long double *r) {
    for (int a = 0; a < d; a++)
        r[a] = 0;

    for (int s = 0; s < sN; s++) {
        for (int t = 0; t < sS[s]; t++) {
            for (int a = 0; a < d; a++)
                r[a] += seqs[s][t][a]*gammas[s][t][i][k];
        }
    }
}

void sumMats(long double ***seqs, long double *mu, long double ****gammas, int d, int sN, int *sS, int i, int k, long double **r) {
    for (int a = 0; a < d; a++) {
        for (int b = 0; b < d; b++)
            r[a][b] = 0;
    }

    for (int s = 0; s < sN; s++) {
        for (int t = 0; t < sS[s]; t++) {
            for (int a = 0; a < d; a++)
                r[a][a] += (seqs[s][t][a]-mu[a])*(seqs[s][t][a]-mu[a])*gammas[s][t][i][k];
        }
    }
}

void mulVect(long double *v, long double a, int d, long double *r) {
    if (a == 0) { // Sum of sums is 0, so each sum is 0
        for (int i = 0; i < d; i++)
            r[i] = 100; // Far far far valueso it's useless
        return;
    }

    for (int i = 0; i < d; i++)
        r[i] = v[i]/a;
}

void mulMat(long double **m, long double a, int d, long double **r) {
    long double s = 0;
    for (int i = 0; i < d; i++)
        s += m[i][i]/a;

    for (int i = 0; i < d; i++) {
        for (int j = 0; j < d; j++) {
            if (i == j) {
                if (m[i][j] <= MIN_VALUE) // Cap min values
                    r[i][j] = MIN_VALUE;
                else
                    r[i][j] = m[i][j]/a;
            }
            else
                r[i][j] = 0;
        }
    }
}

class ContinuousMarkov {
public:
    ContinuousMarkov(std::string name, int n, int m, int d, long double *PI, long double**A, long double **C, long double ***G_mu, long double ****G_sigma);
    ~ContinuousMarkov();

    void render();

    long double calcGaussianValue(long double **sigma, long double *mu, long double *x); // Calculates a single probability for a vector x_ in the gaussian sigma
    void calcProbabilitiesVector(long double *x, long double *r); // Calculate a probability for a vector x in each state's mixture
    void calcProbabilitiesSequence(long double **seq, int s, long double **prob); // Calculate probabilities for each vector of the sequence seq
    long double forward(long double **seq, int s, long double **prob, long double **alpha); // Implementation of the forward algorithm, returns the overall probability of the sequence
    void backward(long double **seq, int s, long double **prob, long double **beta); // Implementation of the backward algorithm (doesn't return overall probability)
    void calcXiOldGamma(long double **seq, int s, long double **alpha, long double **beta, long double p, long double **prob, long double ***xi, long double **oldGamma); // Calculates Xis and Old Gammas for latter calculus
    void calcGamma(long double **seq, int s, long double **alpha, long double **beta, long double **prob, long double ***gamma); // Calculates gamma for latter calculus
    void calcSums(long double ***seqs, int sN, int *sS, long double ****gammas, long double **littleSums, long double ***littleVect, long double ****littleMat, long double *fatSums); // Calculates partial sums for latter calculus
    double baumWelch(long double ***seqs, int sN, int *sS, int maxIt = 100, int epsilon = 0.0000000001); // Baum-Welch Algorithm Implementation, learning algorithm

    std::string name;

    int n;
    int m;
    int d;
    long double *PI;
    long double **A;
    long double **C;
    long double ***G_mu;
    long double ****G_sigma;
};

ContinuousMarkov::ContinuousMarkov(std::string name, int n, int m, int d, long double *PI, long double **A, long double **C, long double ***G_mu, long double ****G_sigma) {
    this->name = name;
    this->n = n;
    this->m = m;
    this->d = d;
    this->PI = PI;
    this->A = A;
    this->C = C;
    this->G_mu = G_mu;
    this->G_sigma = G_sigma;
}

ContinuousMarkov::~ContinuousMarkov() {
}

void ContinuousMarkov::render() {
    std::cout << "Markov's Continuous Automat : " << name << std::endl;
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

void ContinuousMarkov::calcProbabilitiesVector(long double *x, long double *r) {
    for (int i = 0; i < n; i++) {
        r[i] = 0;
        for (int j = 0; j < m; j++)
            r[i] += C[i][j]*calcGaussianValue(G_sigma[i][j], G_mu[i][j], x);
    }
}

void ContinuousMarkov::calcProbabilitiesSequence(long double **seq, int s, long double **prob) {
    for (int i = 0; i < s; i++)
        calcProbabilitiesVector(seq[i], prob[i]);
}

long double ContinuousMarkov::forward(long double **seq, int s, long double **prob, long double **alpha) {
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

    long double p = 0;
    for (int i = 0; i < n; i++)
        p += alpha[s-1][i];

    return p;
}

void ContinuousMarkov::backward(long double **seq, int s, long double **prob, long double **beta) {
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

void ContinuousMarkov::calcGamma(long double **seq, int s, long double **alpha, long double **beta, long double **prob, long double ***gamma) {
    for (int t = 0; t < s; t++) {
        long double sumAB = 0;
        for (int i = 0; i < n; i++)
            sumAB += alpha[t][i]*beta[t][i];

        for (int i = 0; i < n; i++) {
            long double AB = alpha[t][i]*beta[t][i]/sumAB;
            for (int k = 0; k < m; k++) {
                if (prob[t][i] == 0) // This means the sum of probabilities is 0, thus a single one of them will be 0 too
                    gamma[t][i][k] = 0;
                else
                    gamma[t][i][k] = AB*C[i][k]*calcGaussianValue(G_sigma[i][k], G_mu[i][k], seq[t])/prob[t][i];
            }
        }
    }
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
                for (int t = 0; t < sS[s]; t++)
                    littleSums[i][k] += gammas[s][t][i][k];
            }
            sumVects(seqs, gammas, d, sN, sS, i, k, littleVect[i][k]);
            sumMats(seqs, G_mu[i][k], gammas, d, sN, sS, i, k, littleMat[i][k]);
            fatSums[i] += littleSums[i][k];
        }
    }
}

double ContinuousMarkov::baumWelch(long double ***seqs, int sN, int *sS, int maxIt, int epsilon) {
    long double oldLike = -1;
    long double like = 1;
    long double mean = 0;
    long double rap = 1;
    int it = 0;
    //bool decrease = false;
    int totalSize = 0;
    for (int s = 0; s < sN; s++)
        totalSize += sS[s];

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

    // Allocation of temporary arrays
    long double ***alphas = (long double***)malloc(sizeof(long double)*totalSize*n);
    long double ***betas = (long double***)malloc(sizeof(long double)*totalSize*n);
    long double *ps = (long double*)malloc(sizeof(long double)*sN);
    long double ***probs = (long double***)malloc(sizeof(long double)*totalSize*n);

    long double ****xis = (long double****)malloc(sizeof(long double)*totalSize*n*n);
    long double ***oldGammas = (long double***)malloc(sizeof(long double)*totalSize*n);
    long double ****gammas = (long double****)malloc(sizeof(long double)*totalSize*n*n);

    for (int s = 0; s < sN; s++) {
        alphas[s] = (long double**)malloc(sizeof(long double)*sS[s]*n);
        betas[s] = (long double**)malloc(sizeof(long double)*sS[s]*n);
        probs[s] = (long double**)malloc(sizeof(long double)*sS[s]*n);
        xis[s] = (long double***)malloc(sizeof(long double)*sS[s]*n*n);
        oldGammas[s] = (long double**)malloc(sizeof(long double)*sS[s]*n);
        gammas[s] = (long double***)malloc(sizeof(long double)*sS[s]*n*n);
        for (int t = 0; t < sS[s]; t++) {
            alphas[s][t] = (long double*)malloc(sizeof(long double)*n);
            betas[s][t] = (long double*)malloc(sizeof(long double)*n);
            probs[s][t] = (long double*)malloc(sizeof(long double)*n);
            xis[s][t] = (long double**)malloc(sizeof(long double)*n*n);
            oldGammas[s][t] = (long double*)malloc(sizeof(long double)*n);
            gammas[s][t] = (long double**)malloc(sizeof(long double)*n*n);
            for (int i = 0; i < n; i++) {
                xis[s][t][i] = (long double*)malloc(sizeof(long double)*n);
                gammas[s][t][i] = (long double*)malloc(sizeof(long double)*n);
            }
        }
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

    long double r = 0;
    long double num = 0;
    long double den = 0;
    while (it < maxIt) {
        for (int s = 0; s < sN; s++)
                calcProbabilitiesSequence(seqs[s], sS[s], probs[s]);

        for (int s = 0; s < sN; s++) {
            ps[s] = forward(seqs[s], sS[s], probs[s], alphas[s]);
            backward(seqs[s], sS[s], probs[s], betas[s]);

            calcXiOldGamma(seqs[s], sS[s], alphas[s], betas[s], ps[s], probs[s], xis[s], oldGammas[s]);
            calcGamma(seqs[s], sS[s], alphas[s], betas[s], probs[s], gammas[s]);
        }

        // Calculation of sums
        calcSums(seqs, sN, sS, gammas, littleSums, littleVect, littleMat, fatSums);

        for (int i = 0; i < n; i++) {
            // Setting PI and A
            r = 0;
            den = 0;
            for (int s = 0; s < sN; s++) {
                r += oldGammas[s][0][i];
                for (int t = 0; t < sS[s]-1; t++)
                    den += oldGammas[s][t][i];
            }
            _PI[i] = r/sN;

            if (den == 0) { // This means the probability to be in state i at time t is 0
                // So probabilities to go from i at t to j at t+1 will be 0 for each j
                for (int j = 0; j < n; j++)
                    _A[i][j] = (long double)(1./n); // Need to put equi-probabilities
            }
            else {
                for (int j = 0; j < n; j++) {
                    num = 0;
                    for (int s = 0; s < sN; s++) {
                        for (int t = 0; t < sS[s]-1; t++)
                            num += xis[s][t][i][j];
                    }
                    _A[i][j] = num/den;
                }
            }

            if (fatSums[i] == 0) { // C will be problematic
                for (int k = 0; k < m; k++)
                    _C[i][k] = (long double)(1./m); // Need to put equi-probabilities
            } else { // Setting C normally
                for (int k = 0; k < m; k++)
                    _C[i][k] = littleSums[i][k]/fatSums[i];
            }

            // Setting G_mu and G_sigma
            for (int k = 0; k < m; k++) {
                mulVect(littleVect[i][k], littleSums[i][k], d, _G_mu[i][k]);
                mulMat(littleMat[i][k], littleSums[i][k], d, _G_sigma[i][k]);
            }
        }

        like = 1;
        mean = 0;
        for (int s = 0; s < sN; s++) {
            like *= ps[s];
            mean += ps[s];
        }

        mean /= sN;
        //std::cout << "Likelyhood : " << like << " (" << mean << ")" << std::endl << std::endl;
        rap = 1;
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

        for (int i = 0; i < n; i++) {
            PI[i] = _PI[i];
            for (int j = 0; j < n; j++)
                A[i][j] = _A[i][j];
            for (int k = 0; k < m; k++) {
                C[i][k] = _C[i][k];

                for (int a = 0; a < d; a++) {
                    G_mu[i][k][a] = _G_mu[i][k][a];
                    G_sigma[i][k][a][a] = _G_sigma[i][k][a][a];
                }
            }
        }

        it++;
    }

    double result = 0;
    if (oldLike == 0)
        result = 0.5;
    else
        result = log10l(oldLike);

    if (it == maxIt) {
        //std::cout << "Ended on max iteration" << std::endl;
        result = 1 - result;
    }/* else {
        if (decrease)
            std::cout << "Ended on decreasing likelyhood" << std::endl;
        else
            std::cout << "Ended on stationary likelyhod" << std::endl;
    }*/

    //std::cout << "HMM '" << name << "' -> final likelyhood (iteration " << it << " of " << maxIt << ") : " << oldLike << " and mean : " << mean << std::endl << std::endl;

    // Freeings
    // Freeing of new model parameters
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            for (int a = 0; a < d; a++)
                free(_G_sigma[i][j][a]);
            free(_G_mu[i][j]);
            free(_G_sigma[i][j]);
        }
        free(_A[i]);
        free(_C[i]);
        free(_G_mu[i]);
        free(_G_sigma[i]);
    }
    free(_PI);
    free(_A);
    free(_C);
    free(_G_mu);
    free(_G_sigma);

    // Freeing of temporary arrays
    for (int s = 0; s < sN; s++) {
        for (int t = 0; t < sS[s]; t++) {
            for (int i = 0; i < n; i++) {
                free(xis[s][t][i]);
                free(gammas[s][t][i]);
            }
            free(alphas[s][t]);
            free(betas[s][t]);
            free(probs[s][t]);
            free(xis[s][t]);
            free(oldGammas[s][t]);
            free(gammas[s][t]);
        }
        free(alphas[s]);
        free(betas[s]);
        free(probs[s]);
        free(xis[s]);
        free(oldGammas[s]);
        free(gammas[s]);
    }
    free(alphas);
    free(betas);
    free(ps);
    free(probs);
    free(xis);
    free(oldGammas);
    free(gammas);

    // Freeing of partial sums
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            for (int a = 0; a < d; a++)
                free(littleMat[i][j][a]);
            free(littleVect[i][j]);
            free(littleMat[i][j]);
        }
        free(littleSums[i]);
        free(littleVect[i]);
        free(littleMat[i]);
    }
    free(littleSums);
    free(littleVect);
    free(littleMat);
    free(fatSums);

    return result;
}

std::vector<ContinuousMarkov*> markovs;

int findMarkov(std::string s) {
    for (unsigned int i = 0; i < markovs.size(); i++) {
        if (markovs.at(i)->name.compare(s) == 0)
            return (int)i;
    }

    std::cout << "HMM '" << s << "' not found !" << std::endl;
    return -1;
}

void createMarkov(boost::python::str _name, int n, int m, int d, boost::python::list _PI, boost::python::list _A, boost::python::list _C, boost::python::list _G_mu, boost::python::list _G_sigma) {
    std::string name = boost::python::extract<std::string>(_name);
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

    ContinuousMarkov *M = new ContinuousMarkov(name, n, m, d, PI, A, C, G_mu, G_sigma);
    markovs.push_back(M);
}

void removeMarkov(boost::python::str _name) {
    std::string name = boost::python::extract<std::string>(_name);
    int id = findMarkov(name);
    if (id == -1)
        return;

    ContinuousMarkov *M = markovs.at(id);
    markovs.erase(markovs.begin()+id);
    delete M;
}

void renderMarkov(boost::python::str _name) {
    std::string name = boost::python::extract<std::string>(_name);
    int id = findMarkov(name);
    if (id != -1)
        markovs.at(id)->render();
}

long double forward(boost::python::str _name, boost::python::list _seq) {
    std::string name = boost::python::extract<std::string>(_name);
    int id = findMarkov(name);
    if (id == -1)
        return -1;

    int s = boost::python::len(_seq);

    long double **seq = (long double**)malloc(sizeof(long double)*s*markovs.at(id)->d);
    for (int t = 0; t < s; t++) {
        seq[t] = (long double*)malloc(sizeof(long double)*markovs.at(id)->d);
        for (int i = 0; i < markovs.at(id)->d; i++)
            seq[t][i] = boost::python::extract<long double>(_seq[t][i]);
    }

    long double p;
    long double **prob = (long double**)malloc(sizeof(long double)*s*markovs.at(id)->n);
    long double **alpha = (long double**)malloc(sizeof(long double)*s*markovs.at(id)->n);
    for (int t = 0; t < s; t++) {
        prob[t] = (long double*)malloc(sizeof(long double)*markovs.at(id)->n);
        alpha[t] = (long double*)malloc(sizeof(long double)*markovs.at(id)->n);
    }

    markovs.at(id)->calcProbabilitiesSequence(seq, s, prob);
    p = markovs.at(id)->forward(seq, s, prob, alpha);

    for (int t = 0; t < s; t++) {
        free(seq[t]);
        free(prob[t]);
        free(alpha[t]);
    }
    free(seq);
    free(prob);
    free(alpha);

    std::cout << "Forward : " << p << std::endl;
    return p;
}

double baumWelch(boost::python::str _name, boost::python::list _seqs, int it) {
    std::string name = boost::python::extract<std::string>(_name);
    int id = findMarkov(name);
    if (id == -1)
        return 0.8;

    int sN = boost::python::len(_seqs);

    int *sS = (int*)malloc(sizeof(int)*sN);
    int totalSize = 0;
    for (int s = 0; s < sN; s++) {
        sS[s] = boost::python::len(boost::python::extract<boost::python::list>(_seqs[s]));
        totalSize += sS[s];
    }

    long double ***seqs = (long double***)malloc(sizeof(long double)*totalSize*markovs.at(id)->d);
    for (int s = 0; s < sN; s++) {
        seqs[s] = (long double**)malloc(sizeof(long double)*sS[s]*markovs.at(id)->d);
        for (int t = 0; t < sS[s]; t++) {
            seqs[s][t] = (long double*)malloc(sizeof(long double)*markovs.at(id)->d);
            for (int i = 0; i < markovs.at(id)->d; i++)
                seqs[s][t][i] = boost::python::extract<long double>(_seqs[s][t][i]);
        }
    }

    double d = markovs.at(id)->baumWelch(seqs, sN, sS, it);

    for (int s = 0; s < sN; s++) {
        for (int t = 0; t < sS[s]; t++) {
            free(seqs[s][t]);
        }
        free(seqs[s]);
    }
    free(seqs);
    free(sS);

    return d;
}

boost::python::str recognize(boost::python::list _seq) {
    int s = boost::python::len(_seq);

    int d = 13;
    long double **seq = (long double**)malloc(sizeof(long double)*s*d);
    for (int t = 0; t < s; t++) {
        seq[t] = (long double*)malloc(sizeof(long double)*d);
        for (int i = 0; i < d; i++)
            seq[t][i] = boost::python::extract<long double>(_seq[t][i]);
    }

    long double p;
    long double maxP = 0;
    std::string maxName;
    long double **prob;
    long double **alpha;

    for (int id = 0; id < (int)markovs.size(); id++) {
        prob = (long double**)malloc(sizeof(long double)*s*markovs.at(id)->n);
        alpha = (long double**)malloc(sizeof(long double)*s*markovs.at(id)->n);
        for (int t = 0; t < s; t++) {
            prob[t] = (long double*)malloc(sizeof(long double)*markovs.at(id)->n);
            alpha[t] = (long double*)malloc(sizeof(long double)*markovs.at(id)->n);
        }

        markovs.at(id)->calcProbabilitiesSequence(seq, s, prob);
        p = markovs.at(id)->forward(seq, s, prob, alpha);

        if (p > maxP) {
            maxP = p;
            maxName = markovs.at(id)->name;
        }

        for (int t = 0; t < s; t++) {
            free(prob[t]);
            free(alpha[t]);
        }
        free(prob);
        free(alpha);
    }

    for (int t = 0; t < s; t++)
        free(seq[t]);
    free(seq);

    return boost::python::str(maxName);
}

BOOST_PYTHON_MODULE(hmm)
{
    using namespace boost::python;
    def("createMarkov", createMarkov);
    def("removeMarkov", removeMarkov);
    def("renderMarkov", renderMarkov);
    def("forward", forward);
    def("baumWelch", baumWelch);
    def("recognize", recognize);
}

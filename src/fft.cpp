#include <boost/python.hpp>
#include <iostream>
#include <cmath>
#include <complex>

typedef std::complex<double> cDouble;

void hello()
{
    std::cout<<"Hello world !";
}

cDouble* listToTab(boost::python::list l)
{
    int N = boost::python::len(l);
    cDouble *t = (cDouble*)malloc(N*sizeof(cDouble));
    for (int i=0;i<N;i++)
        t[i] = boost::python::extract<cDouble>(l[i]);
    return t;
}

cDouble** listOfListToTab(boost::python::list l)
{
    int N = boost::python::len(l);
    cDouble** t = (cDouble**)malloc(N*sizeof(cDouble*));
    for (int i=0;i<N;i++)
        t[i] = listToTab(boost::python::extract<boost::python::list>(l[i]));
    return t;
}

bool is2Power(int N) { return N==1 || (N%2==0 && is2Power(N/2)); }

int get2Power(int N) { return pow(2, ceil(log(N)/log(2))); }

cDouble e(int k, int N) { return exp((cDouble)(-2j*M_PI*k/N)); }

boost::python::list tabToList(cDouble *t, int N)
{
    boost::python::list l = boost::python::list();
    for (int i=0;i<N;i++)
        l.append(t[i]);
    return l;
}

cDouble* fftCT(cDouble *sig)
{
    //int iMax = (int)(log(N)/log(2));
    int i,j,k,p=0,f=1;
    int N = 1024;
    cDouble ekN;
    cDouble **tmp = (cDouble**)malloc(2*sizeof(cDouble*));

    for (i=0;i<2;i++)
        tmp[i] = (cDouble*)malloc(N*sizeof(cDouble));
    for (i=0;i<N;i++)
        tmp[0][i] = sig[i];
    for (i=N/2;i!=1;i/=2)
    {
        for (j=0;j<i;j++)
            for (k=0;k<N/(2*i);k++)
            {
                ekN = e(k,N/i)*tmp[p][i*(2*k+1)+j];
                tmp[f][i*k+j] = tmp[p][i*(2*k)+j] + ekN;
                tmp[f][i*k+j+N/2] = tmp[p][i*(2*k)+j] - ekN;
            }
        p = f;
        f = (p+1)%2;
    }
    return tmp[p];
}

cDouble* fft(cDouble *sig, int N, int *sizeC, bool mid = false)
{
    //int N = sizeof(sig)/sizeof(cDouble);
    //M = len(sig2)
    //if (M==0 or M==N):
        //if sig2==[]:
            std::cout << "FFT !" << std::endl;
            cDouble* C;
            if (is2Power(N)) {
                std::cout << "2^n" << std::endl;
                C = fftCT(sig);
            } else {
                std::cout<<"zPad needed";
                int NPadded = get2Power(N);
                cDouble* sigPadded = (cDouble*)malloc(NPadded*sizeof(cDouble));
                for (int i=0;i<N;i++)
                    sigPadded[i] = sig[i];
                for (int i=N;i<NPadded;i++)
                    sigPadded[i] = 0;
                C = fftCT(sigPadded);
            }

            if (mid) {
                int n = 512;
                cDouble *rep = (cDouble*)malloc(n*sizeof(cDouble));
                for (int i=0;i<n;i++)
                    rep[i] = C[i];
                *sizeC = n;
                return rep;
            } else {
                *sizeC = N;
                return C;
            }

        //else:
            /*C = fftCT([sig[k]+sig2[k]*1j for k in range(N)],lin)
C1 = [(C[k]+C[N-k].conjugate())/2 for k in range(1,N)]
C2 = [(C[k]-C[N-k].conjugate())/(2j) for k in range(1,N)]
if mid: return C1[len(C1)/2:],C2[len(C2)/2:]
else: return C1,C2
//else:
print "Deux echantillons de meme taille needed !"
return [],[]*/
}

boost::python::list fftListe(boost::python::list pyEchs)
{
    int nbEchs = boost::python::len(pyEchs);
    cDouble **echs = listOfListToTab(pyEchs);
    std::cout << "nbEchs : " << nbEchs << std::endl;
    boost::python::list rep = boost::python::list();
    std::cout << "salope" << std::endl;

    cDouble bla[] = {1, 2};
    int sizeC;
    cDouble* C;

    for (int i=0;i<nbEchs-1;i++)
    {
        std::cout<<"Traitement du " << i << "eme echantillon" << std::endl;
        C = fft(echs[i], 1024, &sizeC);
        rep.append(tabToList(C, sizeC));
    }
    std::cout << "dernier !" << std::endl;

    int a  = boost::python::len(pyEchs[nbEchs-1]);
    std::cout << "list size : " << a << std::endl;
    C = fft(echs[nbEchs-1], a, &sizeC);
    std::cout << "sizeC : " << sizeC << std::endl;
    rep.append(tabToList(C, sizeC));

    std::cout << "end !" << std::endl;
    return rep;
}

/*def fftListe(echs):
n = len(echs)
rep = [[] for k in range(n)]
if n%2 == 1:
for k in range(n/2):
print "Echantillons ",2*k," et ",2*k+1," en cours..."
rep[2*k],rep[2*k+1] = fft(echs[2*k],echs[2*k+1])

else:
for k in range(n/2-1):
print "Echantillons ",2*k," et ",2*k+1," en cours..."
rep[2*k],rep[2*k+1] = fft(echs[2*k],echs[2*k+1])
print "Echantillon ",n-2," en cours..."
rep[n-1] = fft(echs[n-2])
print "Echantillon ",n-1," en cours..."
rep[n-1] = fft(echs[n-1])
return rep

*/

BOOST_PYTHON_MODULE(fft_c)
{
    using namespace boost::python;
    def("hello", hello);
    def("fftListe", fftListe);
}

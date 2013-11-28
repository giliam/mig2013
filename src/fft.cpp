#include <boost/python.hpp>
#include <iostream>
#include <cmath>

void hello()
{
	std::cout<<"Hello world !";
}

boost::python::list fftListe(boost::python::list pyEchs)
{
	double[][] echs = listOfListToTab(pyEchs);
	int nbEchs = pyEchs.count();
	boost::python::list rep = boost::python::list();
	
	for (int i=0;i<nbEchs;i++)
	{
		std::cout<<"Traitement du " + i + "eme echantillon";
		rep.append(tabToList(fft(echs[i])));
	}
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

double[] fft(double[] sig, mid=true)
{
	int N = sizeof(sig)/sizeof(double);
    //M = len(sig2)
    //if (M==0 or M==N):
        //if sig2==[]:
			if (is2Power(N))
				C = fftCT(sig);
			else
				std::cout<<"zPad needed";
				NPadded = get2Power(N);
				double[] sigPadded = malloc(NPadded*sizeof(double));
				for (int i=0;i<N;i++)
					sigPadded[i] = sig[i];
				for (int i=N;i<NPadded;i++)
					sigPadded[i] = 0;
				C = fftCT(sigPadded);
            if mid:
				int n = (sizeof(C)/sizeof(double))/2;
                double[] rep = malloc(n*sizeof(double));
				for (int i=0;i<n;i++)
					rep[i] = C[i];
				return rep;
            else:
                return C;
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
    
double[] fftCT(double[] sig)
{
    int N = sizeof(sig)/sizeof(double);
	int iMax = (int)(log(N)/log(2));
	int i,j,k,p=0,f=1;
	double[][] tmp = malloc(2*sizeof(double*));
	
	for (i=0;i<2;i++)
		tmp[i] = malloc(N*sizeof(double));
	for (i=0;i<N;i++)
		tmp[0][i] = sig[i];
	for (i=N/2;i!=1;i/=2)
	{
		for (j=0;j<i;j++)
			for (k=0;k<N/(2*i);k++)
			{
				ekN = e(k,N)*tmp[p][i*(2*k+1)+j];
				tmp[f][i*k+j] = tmp[p][i*(2*k)+j] + ekN;
				tmp[f][i*k+j+N/2] = tmp[p][i*(2*k)+j] - ekN;
			}
		p = f;
		f = (p+1)%2;
	}
	return tmp[p];
}
			   
bool is2Power(int N)
	return N==1 || (N%2==0 && is2Power(N/2));

int get2Power(int N)
	return pow(2, ceil(log(N)/log(2)));

double e(k,N)
	return exp(-2j*PI*k/N);

boost::python::list tabToList(double[] t)
{
	boost::python::list l = boost::python::list();
	int N = sizeof(t)/sizeof(double);
	for (int i=0;i<N;i++)
		l.append(t[i]);
	return l;
}

double[][] listOfListToTab(boost::python::list l)
{
	int N = l.count();
	double[][] t = malloc(N*sizeof(double*));
	for (int i=0;i<N;i++)
		t[i] = listToTab(l.pop());
	return t;
}

double[] listToTab(boost::python::list l)
{
	int N = l.count();
	double[] t = malloc(N*sizeof(double));
	for (int i=0;i<N;i++)
		t[i] = l.pop();
	return t;
}

BOOST_PYTHON_MODULE(fft)
{
	using namespace boost::python;
	def("hello", hello);
	def("fftListe", fftListe);
}

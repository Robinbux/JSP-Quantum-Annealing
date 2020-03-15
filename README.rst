===================
Job Shop Scheduling
===================
Solver for the `Job Shop Problem <https://en.wikipedia.org/wiki/Job_shop_scheduling>`_ on a
`D-Wave <https://www.dwavesys.com/take-leap>`_ QPU. The constraints for this implementation are based on
`this paper <https://arxiv.org/abs/1506.08479>`_, by Davide Venturelli, Dominic J.J. Marchand and Galo Rojo.

Usage
-----
::

  usage: JSP.py [-h] [-a] [-r] [-v] [-m] [-s] [-q] [-i] [-p]

    optional arguments:
      -h, --help           show this help message and exit
      -a, --automatically  Automatically increase 'Eta', 'Alpha' and 'Beta', until
                           no constraint is violated anymore.
      -r, --replace        Replace old values in the yaml file, with the
                           automatically chosen ones.
      -v, --verbose        More verbose output.
      -m, --matrix         Show an interactive confusion matrix of the final Q.
      -s, --simulated      Use the simulated annealer
      -q, --quantum        Use the D-Wave quantum computer
      -i, --inspect        Use the D-Wave inspector
      -p, --plot           Plot the graph


Hamiltonian
-----------
We have 3 constraints as discribed in the paper.

The first one ensures the order of operations in a job

.. math::

    h_1(\bar{x}) &= \sum_n \left( \sum\limits_{\substack{k_{n-1}<i<k_n \\ t+p_i>t'}} x_{i,t}x_{i+1,t'}\right),

\section{Space Minimization -- Machine level}

For all machines $m$, we want the total length of the starting time in addition to the processing time to be minimal:

\begin{equation*}
\sum_m\left(\sum_{i\in I_m}\sum\limits_{\substack{k\in I_m\\k\neq i\\t'>t}}x_{i,t}x_{k,t'}(t'-(t+p_i))\right)
\end{equation*}


\section{Space Minimization -- Job level}

We want to have the same minimization on the job level:

\begin{equation*}
\sum_n\left(\sum_{k_{n-1}<i<k_n}x_{i,t}x_{i+1,t'}(t'-(t+p_i))\right)
\end{equation*}
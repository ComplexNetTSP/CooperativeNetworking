=======
Example
=======

Generate a Levy-Walk
====================

.. code-block:: python

	import pylab as plt
	from complex_systems.mobility.levy_flight import levy_flight

	LF = levy_flight(alpha=0.66,beta=0.99,sample_length=10,size_max=10000,velocity=1.0,f_min=8,f_max=10000,s_min=0.8,s_max=430,duration=500,b_c=1)
	
	plt.figure()
	plt.plot(LF[0], LF[1], 'o-')

<div style="text-align:center">
<a href="http://www.dmi.unict.it/"><img src="img/unict.png" width="15%" hspace="5" target="_blank"></a>
<a style="margin-left:2%" href="http://www.unica.it/"><img src="img/unica.png" width="16%" hspace="5" target="_blank"></a>
<a style="margin-left:2%" href="https://www.ictlab.srl/"><img src="img/ictlab.png" width="20%" target="_blank"></a>
<a href="https://iplab.dmi.unict.it/"><img src="img/iplab.png" width="9%" hspace="50" target="_blank"></a>
</div>
<br><br>

<h1  style="font-family: Arial;  font-size: 40px;"><b>Computational data analysis for first quantization estimation on JPEG double compressed images</b></h1>

<div style="font-size:15px; color:black"><b><a href="https://www.micc.unifi.it/icpr2020/" target="_blank">In Proceedings of the International Conference on Pattern Recognition</a></b></div>
<br>

<div style="font-size:15px; color:black"><b>Sebastiano Battiato<sup>1,2</sup>, Oliver Giudice<sup>2,3</sup>, Francesco Guarnera<sup>1,2</sup>, Giovanni Puglisi<sup>4</sup></b></div>
<br>
<div style="font-size:12px; color:black"><sup><b>1</b></sup> <em>Department of Mathematics and Computer Science, University of Catania, Viale Andrea Doria 6, Catania 95125, Italy</em><br>
	<sup><b>2</b></sup> <em>iCTLab s.r.l. Spinoff of University of Catania, Italy</em><br>
	<sup><b>3</b></sup> <em>Banca d'Italia, Rome, Italy</em><br>
	<sup><b>4</b></sup> <em>Department of Mathematics and Computer Science, University of Cagliari, Via Ospedale 72, Cagliari 09124, Italy</em><br>
	<br>
	<b>battiato@dmi.unict.it, oliver.giudice@bancaditalia.it, francesco.guarnera@unict.it, puglisi@unica.it</b>
	<br><br>
</div>
<div style="text-align: center; background-color: cornsilk; border-radius: 10px;margin-left: 20%;margin-right: 20%;width: 60%">

<center>
<a href="https://ieeexplore.ieee.org/document/9412528"><font size="5px" ><b>DOWNLOAD PAPER</b></font></a>
</center>
<br><br>
<div style="text-align:left !important;margin-left:20%">
	@article{battiato2021computational,<br>
<span style="margin-left: 2%">title={Computational data analysis for first quantization estimation on JPEG double compressed images},</span><br>
<span style="margin-left: 2%">author={Battiato, Sebastiano and Giudice, Oliver and Guarnera, Francesco and Puglisi, Giovanni},</span><br>
<span style="margin-left: 2%">booktitle={2020 25th International Conference on Pattern Recognition (ICPR)},</span><br>
<span style="margin-left: 2%">pages={5951--5958}</span><br>
<span style="margin-left: 2%">year={2021}</span><br>
<span style="margin-left: 2%">organization = {IEEE}</span><br>
	}
</div>

<br><br>

# Primary JPEG Quantization Estimation 

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details. You should have received a copy of the GNU General Public License along with this program.
If not, see <http://www.gnu.org/licenses/>.

If you are using this software, please cite:

Y.Niu, B. Tondi, Y.Zhao, M.Barni:
“Primary Quantization Matrix Estimation of Double Compressed JPEG Images via CNN",
IEEE Signal Processing Letters, 2019, November
Available on ArXiv: [arXiv preprint:1908.04259](https://arxiv.org/abs/1908.04259)
    
The software estimates the primary quantization matrix of a Double JPEG image (either aligned and not aligned) 
based on a Convolutional Neural Network. The CNN-based estimator works with a 64x64 input patch size. 
The first 15 coefficients of the primary quantization matrix, in zig zag order, are returned by the software.

A model is trained for a fixed quality of the second JPEG compression QF2.

<br>

## Installing dependencies

To install the packages required by our software, you may use the provided *requirements.txt*:
```
cd CnnJpegPrimaryQuantizationEstimation
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r resources/requirements.txt
```
We tested our codes on Python 3.5 and Python 3.6 under Ubuntu 16.04 and 18.04 (64 bit).





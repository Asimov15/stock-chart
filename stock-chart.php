<?php
/* David Zuccaro 29/05/2016 */
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
	<?php 
		function RandomString()
		{
			$characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
			$randstring = '';
			for ($i = 0; $i < 10; $i++) 
			{
				$randstring = $randstring . $characters[rand(0, strlen($characters))];
			};

			return $randstring;
		};			
		$outfn = RandomString() . ".png";
		if (isset($_GET["submit"])) 
		{
			$ecode = $_GET['ecode'];			
			$scode = $_GET['scode'];			
		}
		else
		{
			$ecode = 'AX';
			$scode = 'NAB';
		}			
		$callp = '/usr/bin/python stock-chart.py ' . $outfn . ' ' . $ecode . ' ' . $scode;      
		exec($callp, $out, $status); 						
		echo
		(
			"<head>		
			<meta http-equiv='Content-Type' content='text/html;charset=utf-8'/>	
			<link rel='stylesheet' type='text/css' href='stock-chart.css' />
			<title>Stock Chart</title>           
			<script type='text/javascript'>
				function setop()
				{
					opt1 = '"
		);
		echo
		(	
					$ecode . 
					"'\n
					radiobtn = document.getElementById(opt1);
					radiobtn.checked = true;				
				}
		</script>		
	</head>	");
		
			
			echo("<body onload='setop()'>\n");

			echo("            <h1 class='dz'>Stock Chart</h1>\n");
		 	
			echo("            <form action='stock-chart.php' method='get'>\n");
			echo("                <div class='validate'>
										<div id='header'>			
										</div>
										<div id='wrapper'>
											<div id='outer1'>
												<input type='radio' name='ecode' value='NYSE' id='NYSE'/>New York Stock Exchange<br/>
												<input type='radio' name='ecode' value='AX'   id='AX'/>Australian Stock Exchange			    
											</div>
											<div id='outer2'>
												<input class='code' type='text' name='scode' value ='" . $scode ."'/>
											</div>
											<div id='outer3'>
												<input type='submit' value='Create Chart' name='submit'/> 
											</div>
										</div>
										<div id='footer'>
										</div>
									</div>
								</form>
								<div class='dz'>
								<img class='dz' src='images/" . $outfn . "'>" .
				 "              </div>
				 				<div class='validate2'>
									<a href='http://jigsaw.w3.org/css-validator/'>
										<img style='border:0;width:88px;height:31px' src='http://jigsaw.w3.org/css-validator/images/vcss' alt='Valid CSS!'/>
									</a>	
												
									<a href='http://validator.w3.org/check?uri=referer'>
										<img src='http://www.w3.org/Icons/valid-xhtml11' alt='Valid XHTML 1.1' height='31' width='88' />
									</a>
								</div>						
							</body>
						</html>"
);
?>

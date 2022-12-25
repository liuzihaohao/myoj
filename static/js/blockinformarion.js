$(function () {
    changecolor();
   $('.wd').addClass('bouncing bounceIn');
   setTimeout(function () {
	   $('.wd').removeClass('bouncing bounceIn');
   },3000);
});
// collor
function changecolor() {
	var colors=['#fda34b','#FD84AD','#009688','#e95c5a','#86ba4b','#86C1B9','#FF6666','#336633','#669966','#993333','#009f5d','#cd7bdd','#019fde','#ff1244','#ff5675','#887ddd','#ff8345'];
	var s=Math.floor(Math.random() * colors.length)
	$(".wd").each(function(i,n){
		if (s>=colors.length){
			s=0;
		};
		$(this).css("background-color",colors[s]);
		console.log(String(colors[s]));
		s=s+1;
	});
};

(function (){
	setInterval(function(){
		changecolor()
	},5000);
})();

// (function(){
// 	$(".wd").on('mouseover',function(){
// 		// console.log($(this).children());
// 		$(this).css('width','120%');
// 		$(this).children().children().css('color','red');
// 	});
// 	$(".wd").on('mouseleave',".top-text",function(){
// 		// console.log($(this).children());
// 		$(this).children().children().css('color','#fff');
// 	});
// })();
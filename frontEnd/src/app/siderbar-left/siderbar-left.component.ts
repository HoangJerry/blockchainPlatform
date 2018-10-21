import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-siderbar-left',
  templateUrl: './siderbar-left.component.html',
  styleUrls: ['./siderbar-left.component.css']
})
export class SiderbarLeftComponent implements OnInit {
	currentUrl: string;
	constructor(private router: Router) {
	  	this.router.events.subscribe((e) => {
		  if (e instanceof NavigationEnd) {
		    this.currentUrl = e.url;
		  }
	});
  }
  ngOnInit() {
  }

}

import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { HttpService } from '../http.service'

@Component({
  selector: 'app-siderbar-left',
  templateUrl: './siderbar-left.component.html',
  styleUrls: ['./siderbar-left.component.css']
})
export class SiderbarLeftComponent implements OnInit {
	currentUser :any;
	currentUrl: string;
	constructor(private http: HttpService, private router: Router) {
	  	this.router.events.subscribe((e) => {
		  if (e instanceof NavigationEnd) {
		    this.currentUrl = e.url;
		  }
	});
  }

  ngOnInit() {
  	this.http.currentUser.subscribe(user => {this.currentUser = user;});
  }

}

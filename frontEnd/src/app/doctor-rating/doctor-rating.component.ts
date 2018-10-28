import { Component, OnInit } from '@angular/core';
import { HttpService } from '../http.service'
import { ToastyService, ToastyConfig, ToastOptions, ToastData } from 'ng2-toasty';
import { Router }                   from '@angular/router'

@Component({
  selector: 'app-doctor-rating',
  templateUrl: './doctor-rating.component.html',
  styleUrls: ['./doctor-rating.component.css']
})
export class DoctorRatingComponent implements OnInit {
  current_rating :any = new Object;
  next_rating :any;
  previous_rating:any;
  getCurrentRating = () =>{
  	this.http.getUserTestHistory('?is_rating=true').subscribe((data:any)=>{
  		this.current_rating=data.results[0];
  		this.next_rating = data.results.slice(1,data.results.length);
  	})

  	this.http.getUserTestHistory('?status=40').subscribe((data:any)=>{
  		this.previous_rating=data.results;
  	})
  }

  constructor(private http: HttpService,
              private toastyService:ToastyService, 
              private router: Router,
              private toastyConfig: ToastyConfig,){
  	this.getCurrentRating();
  }

  onChangeStar = (data) =>{
  	console.log(data);
  	this.current_rating.doctor_star=data;
  	this.http.updateUserTestHistory(this.current_rating).subscribe((s)=>{this.getCurrentRating();});
  	
  }

  ngOnInit() {
  }



}

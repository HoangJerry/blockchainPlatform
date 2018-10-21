import { Component, OnInit } from '@angular/core';
import { HttpService } from '../http.service'
@Component({
  selector: 'app-health-care-record',
  templateUrl: './health-care-record.component.html',
  styleUrls: ['./health-care-record.component.css']
})
export class HealthCareRecordComponent implements OnInit {
  user:any;
  userTestHistories:any;
  constructor(private http:HttpService) {
  	this.http.getUserInfor().subscribe((data)=>{
  		this.user = data
  	})

  	this.http.getUserTestHistory().subscribe((data:any)=>{
  		this.userTestHistories = data.results;
  		console.log(data);
  	})
  }

  ngOnInit() {
  }

  onChangeUser(){
  	this.http.updateUser(this.user)
  }
}

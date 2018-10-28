import { Component, OnInit } from '@angular/core';
import { HttpService } from '../http.service'
@Component({
  selector: 'app-health-care-record',
  templateUrl: './health-care-record.component.html',
  styleUrls: ['./health-care-record.component.css']
})
export class HealthCareRecordComponent implements OnInit {
  user:any = new Object;
  userTestHistories:any;
  doctorTestHistories:any;
  constructor(private http:HttpService) {
  	this.http.getUserInfor().subscribe((data)=>{
  		this.user = data;
      if (this.user.role==0){
        this.http.getDoctorTestHistory().subscribe((d:any)=>{
          this.doctorTestHistories=d.results;
        })
      }
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

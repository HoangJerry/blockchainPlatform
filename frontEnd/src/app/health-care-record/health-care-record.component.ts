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
  selected:any
  constructor(private http:HttpService) {
  	this.getStart();
  }

  ngOnInit() {
  }
  getStart = () =>{
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
  onChangeUser(){
  	this.http.updateUser(this.user)
  }
  onSubmit = () =>{
    this.http.updateUserTestHistory(this.selected).subscribe((data)=>this.getStart())
  }
  onChangeResult = (test) => {
    this.selected=test;
  }
}

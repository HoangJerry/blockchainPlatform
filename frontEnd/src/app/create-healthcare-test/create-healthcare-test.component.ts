import { Component, OnInit } from '@angular/core';
import { HttpService } from '../http.service'
import { ToastyService, ToastyConfig, ToastOptions, ToastData } from 'ng2-toasty';
import { Router }                   from '@angular/router'
import {ModalModule} from "ng2-modal";

@Component({
  selector: 'app-create-healthcare-test',
  templateUrl: './create-healthcare-test.component.html',
  styleUrls: ['./create-healthcare-test.component.css']
})
export class CreateHealthcareTestComponent implements OnInit {
  currentUser :any;
  test:object = new Object;
  name_of_test_show:any;
  constructor(private http: HttpService,
              private toastyService:ToastyService, 
              private router: Router,
              private toastyConfig: ToastyConfig,) {
    this.toastyConfig.theme = 'material';
  	this.http.getNameOfTest().subscribe((data)=>{
  		this.name_of_test_show =data;
  		console.log(this.name_of_test_show);

  	})

  }

  ngOnInit() {
    this.http.currentUser.subscribe(user => {this.currentUser = user;});
  }

  onClickCreate = () => {
  	this.http.createTestHistory(this.test).subscribe(
  		(data)=>{
        	this.toastyService.success("Create success!");
  			this.router.navigate(['/health-care-record']);
  		},
  		(error)=>{
  			if (error.error.detail!=undefined){
                    this.toastyService.error(error.error.detail);
                }
            else{
            	for( let key in error.error){
            		console.log(key);
	                let x = 'error.error.'+key;
	                this.toastyService.error(key.toUpperCase()+": "+eval(x)[0]);
	            }
            }
            
  		})
  }
}

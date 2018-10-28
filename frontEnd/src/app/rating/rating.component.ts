import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-rating',
  templateUrl: './rating.component.html',
  styleUrls: ['./rating.component.css']
})
export class RatingComponent implements OnInit {
  @Input() 
  set selectedData(name: any) {
    this.selected = name;
  }
  selected:any;
  @Output() changeSelected: EventEmitter<string> =   new EventEmitter();
  constructor() { }

  ngOnInit() {
  }

  onChangeStar = (star) => {
  	this.selected.doctor_start = star;
  	this.changeSelected.emit(this.selected.doctor_start);
  }


}

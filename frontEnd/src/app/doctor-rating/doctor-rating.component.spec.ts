import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DoctorRatingComponent } from './doctor-rating.component';

describe('DoctorRatingComponent', () => {
  let component: DoctorRatingComponent;
  let fixture: ComponentFixture<DoctorRatingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DoctorRatingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DoctorRatingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

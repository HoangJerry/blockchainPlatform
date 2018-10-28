import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateHealthcareTestComponent } from './create-healthcare-test.component';

describe('CreateHealthcareTestComponent', () => {
  let component: CreateHealthcareTestComponent;
  let fixture: ComponentFixture<CreateHealthcareTestComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateHealthcareTestComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateHealthcareTestComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

#version 330


uniform sampler2D tex;

out vec4 pixelColor; //Output variable of the fragment shader. (Almost) final pixel color.

//Varying variables
in vec2 i_tc;
in vec4 n;
in vec4 v;

in vec4 listc[5];

vec4 ml[5];
vec4 mr[5];
float rv[5];
float i_nl[5];

vec4 mn;
vec4 mv;
vec4 kd;
vec4 ks;
vec4 color;

void computeLightMore(){
    pixelColor = vec4(0,0,0,0);
	mn = normalize(n);
	mv = normalize(v);
	kd = texture(tex,i_tc);
	ks = kd;
    color=texture(tex,i_tc);
    for (int y =0;y<5;y++){
        ml[y] = normalize(listc[y]);
        mr[y] = reflect(-ml[y],mn);
        rv[y] = pow(clamp(dot(mr[y],mv),0,1),20);
        i_nl[y] = clamp(dot(mn,ml[y]),0,1);
        pixelColor += (vec4(kd.rgb * i_nl[y],kd.a)+vec4(ks.rgb*rv[y],0)) * 0.25;
    }    
}

void main(void) {

    computeLightMore();

}

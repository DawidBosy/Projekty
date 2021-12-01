#version 330

//Uniform variables
uniform mat4 P;
uniform mat4 V;
uniform mat4 M;
uniform vec4 list[5];

//Attributes
layout (location=0) in vec4 vertex; //vertex coordinates in model space
layout (location=1) in vec4 normal; //vertex normal vector in model space
layout (location=2) in vec2 texCoord; //texturing coordinates


//varying variables
out vec2 i_tc;
out vec4 listc[5];

out vec4 n;
out vec4 v;

void computeLight(){
    for(int x = 0;x<5;x++){
        listc[x] = normalize(V*list[x]-V*M*vertex);
    }
}

void main(void) {

    computeLight();

    mat4 G=mat4(inverse(transpose(mat3(M))));
    n=normalize(V*G*normal);

    v = normalize(vec4(0,10,0,1)-V*M*vertex);
    
    i_tc=texCoord;
    
    gl_Position=P*V*M*vertex;

}
